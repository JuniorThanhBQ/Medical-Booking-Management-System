import re

from flask import current_app, request
from flask_restx import Resource, fields

from src.libs.email_validator import verify_email_existence
from src.middlewares.auth import auth_required
from src.modules.users import auth_namespace
from src.modules.users.services import (get_user_data, is_email_available,
                                        login_user_service,
                                        register_user_service,
                                        update_patient_profile_service)
from src.utils.utils import (EMAIL_REGEX, check_xss_violation,
                             format_api_response, generate_username,
                             get_request_data, validate_email_password)

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
    def post(self):
        data = get_request_data(request)
        login_email = data.get("email")
        password = data.get("password")
        role = data.get("role")

        if not all([login_email, password, role]):
            return {"message": "Vui lòng điền đầy đủ email, mật khẩu và vai trò"}, 400

        invalid_input = validate_email_password(login_email, password)
        if invalid_input:
            return invalid_input, 400

        return format_api_response(*login_user_service(login_email=login_email,
                                                       password=password,
                                                       role=role),
                                   success_code=201)


class RegisterAPI(Resource):
    @auth_namespace.expect(register_payload)
    def post(self):
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
            return {"message": "Email không tồn tại trong thực tế"}, 400

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

        return format_api_response(*register_user_service(user_payload),
                                   success_code=201)


class EmailValidatorAPI(Resource):
    @auth_namespace.expect(email_validator_payload)
    def post(self):
        data = get_request_data(request)
        email = data.get("email")

        if not email:
            return {"message": "Vui lòng cung cấp email"}, 400

        if not re.match(EMAIL_REGEX, email):
            return {"is_valid": False, }, 400

        is_valid = is_email_available(email)

        if not is_valid:
            return {"is_valid": is_valid, }, 400

        return {"is_valid": is_valid, }, 201


class RetrieveCurrentUserAPI(Resource):
    method_decorators = [auth_required]

    @auth_namespace.doc(security='api_key')
    def get(self, current_user):
        user_data = get_user_data(current_user)

        if not user_data:
            return {"message": "Có vấn đề trong lấy thông tin người dùng"}, 500

        return {
            "message": "Lấy thông tin thành công",
            "user": user_data,
        }, 200

    @auth_namespace.doc(security='api_key')
    @auth_namespace.expect(patch_user_payload)
    def patch(self, current_user):
        data = get_request_data(request)
        data["avatar"] = request.files.get("avatar") or data.get("avatar")

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(*update_patient_profile_service(
            current_user=current_user, data=data), success_code=200)
