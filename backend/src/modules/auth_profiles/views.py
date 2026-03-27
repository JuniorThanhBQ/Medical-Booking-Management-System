import re

from flask import request
from flask_restx import Namespace, Resource, fields

from src.extensions import limiter
from src.middlewares.auth import token_required
from src.modules.auth_profiles.services import (check_email_exists_service,
                                                get_user_data,
                                                login_user_service,
                                                register_user_service,
                                                update_patient_profile_service)
from src.utils.utils import (EMAIL_REGEX, check_xss_violation,
                             generate_username, get_http_status_code,
                             get_request_data, validate_email_password)

auth_namespace = Namespace("auth", description="API liên quan đến tài khoản người dùng")

login_model = auth_namespace.model('LoginInput', {
    'email': fields.String(required=True),
    'password': fields.String(required=True),
    'role': fields.String(required=True)
})

register_model = auth_namespace.model('RegisterInput', {
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

patch_user_model = auth_namespace.model('PatchUserInput', {
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

email_validator_model = auth_namespace.model('EmailValidatorInput', {
    'email': fields.String(required=True)
})


class LoginAPI(Resource):
    decorators = [limiter.limit("10 per minute")]

    @auth_namespace.expect(login_model)
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

        token, user_data, http_status = login_user_service(login_email, password, role)

        if not token:
            if http_status == "ERROR_UNAUTHORIZED":
                return ({"message": "Sai tên đăng nhập hoặc mật khẩu"},
                        get_http_status_code(http_status))
            return ({"message": "Tài khoản không có thẩm quyền truy cập"},
                    get_http_status_code(http_status))

        return {
            "message": "Đăng nhập thành công",
            "access_token": token,
            "user": user_data,
        }, 200


class RegisterAPI(Resource):
    decorators = [limiter.limit("10 per minute")]

    @auth_namespace.expect(register_model)
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
            return {"message": "Vui lòng cung cấp đầy đủ các thông tin bắt buộc"}, 400

        data_fields = [
            username, password, email, first_name, last_name, address, birthday, gender, phone,
            medical_history
        ]

        if check_xss_violation(data_fields):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        invalid_input = validate_email_password(email, password)
        if invalid_input:
            return invalid_input, 400

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

        user_data, status_type = register_user_service(user_payload)

        if not user_data:
            return ({"message": "Sai định dạng ngày sinh hoặc email đã tồn tại"},
                    get_http_status_code(status_type))

        return {
            "message": "Đăng ký thành công",
            "user": user_data,
        }, 201


class EmailValidatorAPI(Resource):
    decorators = [limiter.limit("50 per minute")]

    @auth_namespace.expect(email_validator_model)
    def post(self):
        data = get_request_data(request)
        email = data.get("email")

        if not email:
            return {"message": "Vui lòng cung cấp email"}, 400

        if not re.match(EMAIL_REGEX, email):
            return {
                "is_valid": False,
            }, 400

        is_valid = check_email_exists_service(email)

        if not is_valid:
            return {
                "is_valid": is_valid,
            }, 400

        return {
            "is_valid": is_valid,
        }, 200


class RetrieveCurrentUserAPI(Resource):
    method_decorators = [token_required]

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
    @auth_namespace.expect(patch_user_model)
    def patch(self, current_user):
        data = get_request_data(request)
        data["avatar"] = request.files.get("avatar") or data.get("avatar")

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        user_data, status_type = update_patient_profile_service(current_user, data)

        if not user_data:
            if status_type == "ERROR_BAD_REQUEST":
                return ({"message": "Sai định dạng ngày sinh hoặc không có hồ sơ"},
                        get_http_status_code(status_type))
            return ({"message": "Chỉ tài khoản bệnh nhân mới được thay đổi hồ sơ"},
                    get_http_status_code(status_type))

        return {
            "message": "Cập nhật hồ sơ thành công",
            "data": user_data,
        }, 200
