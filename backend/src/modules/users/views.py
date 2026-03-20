from flask import Blueprint, request
from flask_restful import Api, Resource
from src.modules.users.services import (get_user_information,
                                        login_google_service,
                                        login_user_service,
                                        register_user_service, token_required,
                                        update_patient_profile_service)

auth_bp = Blueprint("auth_v1", __name__, url_prefix="/api/v1/auth")
api = Api(auth_bp)


class RegisterAPI(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = request.get_json(silent=True) or request.form
        username = data.get("username")
        password = data.get("password")
        email = data.get("email")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        birthday = data.get("birthday")
        gender = data.get("gender")
        phone = data.get("phone")
        avatar = request.files.get("avatar") or data.get("avatar")

        if not all(
            [username, password, email, first_name, last_name, gender, phone, birthday]
        ):
            return {"message": "Vui lòng điền đầy đủ thông tin bắt buộc"}, 400

        user_data, message, status_type = register_user_service(
            username,
            password,
            email,
            first_name,
            last_name,
            avatar,
            birthday,
            gender,
            phone,
        )

        if not user_data:
            status = 500 if status_type == "SERVER_INTERNAL_ERROR" else 400
            return {"message": message}, status

        return {
            "message": message,
            "user": user_data,
        }, 201


class LoginAPI(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = request.get_json(silent=True) or request.form
        login_type = data.get("username") or data.get("email")
        password = data.get("password")

        if not login_type or not password:
            return {"message": "Username/Email và password không được để trống"}, 400

        token, message, status_type = login_user_service(login_type, password)

        if not token:
            status = 403 if status_type == "FORBIDDEN" else 401
            return {"message": message}, status

        return {
            "message": message,
            "token": token,
        }, 200


class GoogleLoginAPI(Resource):
    # noinspection PyMethodMayBeStatic
    def post(self):
        data = request.get_json(silent=True) or request.form
        token = data.get("token")

        if not token:
            return {"message": "Google token không được để trống"}, 400

        result, error = login_google_service(token)

        if error:
            return {"message": error}, 401

        return {
            "message": "Đăng nhập Google thành công",
            "token": result["token"],
        }, 200


class CurrentUserAPI(Resource):
    method_decorators = [token_required]

    # noinspection PyMethodMayBeStatic
    def get(self, current_user):
        return {
            "message": "Lấy thông tin thành công",
            "data": get_user_information(current_user),
        }, 200

    # noinspection PyMethodMayBeStatic
    def patch(self, current_user):
        data = request.get_json(silent=True) or request.form
        user_data, message, status_type = update_patient_profile_service(
            current_user, data
        )

        if not user_data:
            if status_type == "SERVER_INTERNAL_ERROR":
                status_code = 500
            elif status_type == "FORBIDDEN":
                status_code = 403
            else:
                status_code = 400
            return {"message": message}, status_code

        return {
            "message": message,
            "data": user_data,
        }, 200


api.add_resource(RegisterAPI, "/register")
api.add_resource(LoginAPI, "/login")
api.add_resource(GoogleLoginAPI, "/google-login")
api.add_resource(CurrentUserAPI, "/current-user")
