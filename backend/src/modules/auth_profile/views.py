import re

from flask import request
from flask_restful import Resource

from src.extensions import limiter
from src.modules.auth_profile.auth_decorators import token_required
from src.modules.auth_profile.services import (check_email_exists_service,
                                               get_user_data,
                                               login_google_service,
                                               login_user_service,
                                               register_user_service,
                                               update_patient_profile_service)
from src.utils.utils import (EMAIL_REGEX, check_xss_violation,
                             get_http_status_code, get_request_data,
                             validate_email_password)


class LoginAPI(Resource):
    decorators = [limiter.limit("5 per minute")]

    def post(self):
        data = get_request_data(request)
        login_email = data.get("email", "")
        password = data.get("password", "")

        error_msg, status_code = validate_email_password(login_email, password)
        if error_msg:
            return error_msg, status_code

        token, message, user_data, http_status = login_user_service(login_email, password)

        if not token:
            return {"message": message}, get_http_status_code(http_status, default=401)

        return {
            "message": message,
            "access_token": token,
            "user": user_data,
        }, 200


class RegisterAPI(Resource):
    decorators = [limiter.limit("10 per minute")]

    def post(self):
        data = get_request_data(request)
        password = data.get("password")
        email = data.get("email")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        username = "newUserMembers"
        address = data.get("address")
        birthday = data.get("dayOfBirth")
        gender = data.get("gender")
        phone = data.get("phone")
        avatar = request.files.get("avatar") or data.get("avatar")
        medical_history = data.get("medicalHistory")

        if not all(
                [password, email, first_name, last_name, gender, phone, birthday, address]
        ):
            return {"message": "Vui lòng điền đầy đủ thông tin bắt buộc"}, 400

        fields = [
            username, password, email, first_name, last_name, address, birthday, gender, phone,
            medical_history
        ]

        if check_xss_violation(fields):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        if len(username) <= 8:
            return {"message": "Username phải có trên 8 ký tự"}, 400

        error_msg, status_code = validate_email_password(email, password)
        if error_msg:
            return error_msg, status_code

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

        user_data, message, status_type = register_user_service(user_payload)

        if not user_data:
            return {"message": message}, get_http_status_code(status_type, default=400)

        return {
            "message": message,
            "user": user_data,
        }, 201


class GoogleLoginAPI(Resource):
    def post(self):
        data = get_request_data(request)
        google_token = data.get("google_token")

        if not google_token:
            return {"message": "Thiếu google_token từ phía client"}, 400

        result, error, status = login_google_service(google_token)

        if error:
            return {"message": error}, 401

        return {
            "message": "Đăng nhập Google thành công",
            "data": result,
            "status": status
        }, 200


class EmailValidatorAPI(Resource):
    decorators = [limiter.limit("15 per minute")]

    def post(self):
        data = get_request_data(request)
        email = data.get("email", "").strip()

        if not email or not re.match(EMAIL_REGEX, email):
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

    def get(self, current_user):
        return {
            "message": "Lấy thông tin thành công",
            "user": get_user_data(current_user),
        }, 200

    def patch(self, current_user):
        data = get_request_data(request)
        data["avatar"] = request.files.get("avatar") or data.get("avatar")

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        user_data, message, status_type = update_patient_profile_service(current_user, data)

        if not user_data:
            return {"message": message}, get_http_status_code(status_type, default=400)

        return {
            "message": message,
            "data": user_data,
        }, 200
