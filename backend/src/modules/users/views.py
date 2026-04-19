import re

from dependency_injector.wiring import Provide, inject
from flask import current_app, make_response, request
from flask_restx import Resource, fields

from src.containers import AppContainer
from src.libs.email_validator import verify_email_existence
from src.middlewares.auth import auth_required
from src.modules.users import auth_namespace
from src.utils.users.jwt_utils import confirm_verification_token
from src.utils.utils import (EMAIL_REGEX, check_xss_violation,
                             format_api_response, generate_username,
                             get_request_data, handle_auth_refresh_response,
                             validate_email_password)

login_payload = auth_namespace.model('LoginInput', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required=True)
})

register_payload = auth_namespace.model('RegisterInput', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'firstName': fields.String(required=True),
    'lastName': fields.String(required=True),
    'dayOfBirth': fields.String(required=True),
    'gender': fields.String(required=True),
    'phone': fields.String(required=True),
    'address': fields.String(),
    'medicalHistory': fields.String(),
    'avatar': fields.String()
})

patch_user_payload = auth_namespace.model('PatchUserInput', {
    'email': fields.String(),
    'firstName': fields.String(),
    'lastName': fields.String(),
    'dayOfBirth': fields.String(),
    'gender': fields.String(),
    'phone': fields.String(),
    'address': fields.String(),
    'medicalHistory': fields.String(),
    'avatar': fields.String()
})

email_validator_payload = auth_namespace.model('EmailValidatorInput', {
    'email': fields.String(required=True)
})


class LoginAPI(Resource):
    @auth_namespace.expect(login_payload)
    @inject
    def post(self, auth_service = Provide[AppContainer.user_app.auth_service]):
        data = get_request_data(request)
        login_email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not all([login_email, password, role]):
            return {"message": "Vui lòng điền đầy đủ email, mật khẩu và vai trò"}, 400

        invalid_input = validate_email_password(login_email, password)
        if invalid_input:
            return invalid_input, 400

        data, status = auth_service.login_user_service(login_email=login_email,
                                          password=password,
                                          role=role)

        return handle_auth_refresh_response(
            data, status,
            success_code=201,
            refresh_token=data.get("refresh_token") if status == "SUCCESS" else None
        )


class RegisterAPI(Resource):
    @auth_namespace.expect(register_payload)
    @inject
    def post(self, auth_service = Provide[AppContainer.user_app.auth_service]):
        data = get_request_data(request)
        password = data.get("password")
        email = data.get("email")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        birthday = data.get("dayOfBirth")
        gender = data.get("gender")
        phone = data.get("phone")
        username = generate_username(first_name, last_name)
        address = data.get("address")
        avatar = request.files.get("avatar") or data.get("avatar")
        medical_history = data.get("medicalHistory")

        if not all([password, email, first_name, last_name, birthday, gender, phone]):
            return {"message": "Vui lòng cung cấp các thông tin bắt buộc"}, 400

        data_payload = [
            username, password, email, first_name, last_name, address, birthday, gender, phone,
            medical_history
        ]

        if check_xss_violation(data_payload):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        invalid_input = validate_email_password(email, password)
        if invalid_input:
            return invalid_input, 400

        if not verify_email_existence(current_app.config.get('EMAIL_VALIDATOR'), email):
            return {"is_valid": False, }, 400

        user_payload = {
            "username": username,
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "avatar": avatar,
            "birthday": birthday,
            "gender": gender,
            "phone": phone,
            "address": address,
            "medical_history": medical_history
        }

        return format_api_response(*auth_service.register_user_service(user_payload),
                                   success_code=201)


class EmailValidatorAPI(Resource):
    @auth_namespace.expect(email_validator_payload)
    @inject
    def post(self, auth_service = Provide[AppContainer.user_app.auth_service]):
        data = get_request_data(request)
        email = data.get("email")

        if not email:
            return {"message": "Vui lòng cung cấp email"}, 400

        if not re.match(EMAIL_REGEX, email):
            return {"is_valid": False, }, 400

        is_available_valid = auth_service.is_email_available(email)
        if not is_available_valid:
            return is_available_valid, 400

        return {"is_valid": is_available_valid, }, 201


class RetrieveCurrentUserAPI(Resource):
    method_decorators = [auth_required]

    @auth_namespace.doc(security='api_key')
    @inject
    def get(self, current_user, user_service = Provide[AppContainer.user_app.profile_service]):
        user_data = user_service.get_user_data(current_user)

        if not user_data:
            return {"message": "Có vấn đề trong lấy thông tin người dùng"}, 500

        return {
            "message": "Lấy thông tin thành công",
            "user": user_data,
        }, 200

    @auth_namespace.doc(security='api_key')
    @auth_namespace.expect(patch_user_payload)
    @inject
    def patch(self, current_user, user_service = Provide[AppContainer.user_app.profile_service]):
        data = get_request_data(request)
        data["avatar"] = request.files.get("avatar") or data.get("avatar")

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(*user_service.update_patient_profile_service(
            current_user=current_user, data=data), success_code=200)


class RefreshTokenAPI(Resource):
    @inject
    def post(self, user_service = Provide[AppContainer.user_app.auth_service]):
        refresh_token = request.cookies.get("refresh_token")
        if not refresh_token:
            return {"message": "Refresh token không tồn tại trong cookie"}, 400

        data, status = user_service.refresh_token_service(refresh_token_str=refresh_token)

        return handle_auth_refresh_response(
            data, status,
            success_code=201,
            refresh_token=data.get("refresh_token") if status == "SUCCESS" else None
        )


class LogoutAPI(Resource):
    method_decorators = [auth_required]

    @auth_namespace.doc(security='api_key')
    def post(self):
        data, status = {"message": "Đăng xuất thành công"}, "SUCCESS"
        response = make_response(format_api_response(data, status), 200)
        if status == "SUCCESS":
            response.delete_cookie("refresh_token")

        return response


class VerifyEmailAPI(Resource):
    @inject
    def post(self, auth_service=Provide[AppContainer.user_app.auth_service]):
        data = request.get_json()
        token = data.get("token")
        if not token:
            return {"message": "Token không được cung cấp"}, 400

        email = confirm_verification_token(token)
        if not email:
            return {"message": "Liên kết xác thực không hợp lệ hoặc đã hết hạn."}, 400

        msg, status = auth_service.activate_user_account(email)

        if status == "SUCCESS":
            return {"message": "Tài khoản đã được kích hoạt thành công. Bạn có thể đăng nhập."}, 200

        return {"message": msg}, 400
