import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from src.libs.cloudinary import cloudinary_upload_process
from src.modules.users.models import PatientProfile, User
from src.modules.users.rabbitmq.tasks import send_verification_email_task
from src.utils.handle_db_errors import handle_db_errors
from src.utils.users.jwt_utils import (create_refresh_token, create_token,
                                       generate_verification_token)
from src.utils.users.profile_utils import (add_profile_updates,
                                           update_extended_profile)
from src.utils.utils import parse_date, parse_gender


class AuthService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    @handle_db_errors
    def login_user_service(self, login_email=None, password=None, role=None):
        user = self.user_repository.get_user_by_email(login_email)

        if not user or not check_password_hash(user.password, password):
            return {"message": "Sai tên đăng nhập hoặc mật khẩu"}, "ERROR_UNAUTHORIZED"

        if not user.is_active:
            return {"message": "Tài khoản bị khoá hoặc chưa xác thực"}, "FORBIDDEN"

        if role.upper() != user.role.name:
            return {"message": "Tài khoản không có thẩm quyền truy cập"}, "FORBIDDEN"

        token = create_token(user=user)
        refresh_token = create_refresh_token(user=user)
        user_data = UserService.get_user_data(user=user)

        if token and refresh_token and user_data:
            data = {
                "message": "Đăng nhập thành công",
                "access_token": token,
                "refresh_token": refresh_token,
                "user": user_data,
            }
            return data, "SUCCESS"

        return {"message": "Lỗi không xác định khi đăng nhập"}, "SERVER_INTERNAL_ERROR"


    @handle_db_errors
    def register_user_service(self, user_payload=None):
        if not user_payload:
            return None, "ERROR_BAD_REQUEST"

        email = user_payload.get("email")
        if self.user_repository.get_user_by_email(email):
            return {"message": "Email đã tồn tại"}, "ERROR_BAD_REQUEST"

        set_birthday, date_err = parse_date(user_payload.get("birthday"))
        if date_err:
            return {"message": date_err}, "ERROR_BAD_REQUEST"

        set_gender = parse_gender(user_payload.get("gender"))

        avatar = user_payload.get("avatar")
        avatar_url = cloudinary_upload_process(avatar) if avatar else None

        new_user = User(
            username=user_payload.get("username"),
            password=generate_password_hash(user_payload.get("password")),
            email=email,
            first_name=user_payload.get("first_name"),
            last_name=user_payload.get("last_name"),
            is_active=False
        )
        self.user_repository.add_user(new_user)

        new_profile = PatientProfile(
            user_id=new_user.id,
            phone=user_payload.get("phone"),
            avatar=avatar_url,
            gender=set_gender,
            birthday=set_birthday,
            address=user_payload.get("address"),
            medical_history=user_payload.get("medical_history"),
        )
        self.user_repository.add_profile(new_profile)
        self.user_repository.commit()

        token = generate_verification_token(new_user.email)
        verification_link = (f"{current_app.config.get("FRONTEND_URL")}"
                             f"/email-verification?token={token}")

        send_verification_email_task.delay(new_user.email, verification_link)

        return {
            "message": "Vui lòng kiểm tra email để kích hoạt tài khoản trong vòng 15 phút."
        }, "SUCCESS"


    def is_email_available(self, email: str):
        user = self.user_repository.get_user_by_email(email)

        return {
            "isExisted": bool(user),
            "role": user.role.name if user else None
        }

    @handle_db_errors
    def refresh_token_service(self, refresh_token_str=None):
        if not refresh_token_str:
            return {"message": "Refresh token không tồn tại"}, "ERROR_UNAUTHORIZED"

        try:
            secret_key = current_app.config.get("SECRET_KEY")
            data = jwt.decode(refresh_token_str, secret_key, algorithms=["HS256"])

            user_id = data.get("user_id")
            if not user_id:
                return {"message": "Payload của refresh token không hợp lệ"}, "ERROR_UNAUTHORIZED"

            user = self.user_repository.get_user_by_id(user_id)

            if not user:
                return {"message": "Người dùng không tồn tại"}, "ERROR_UNAUTHORIZED"

            if not user.is_active:
                return {"message": "Tài khoản bị khoá hoặc chưa xác thực"}, "FORBIDDEN"

            new_access_token = create_token(user=user)
            new_refresh_token = create_refresh_token(user=user)

            if new_access_token and new_refresh_token:
                data_response = {
                    "message": "Tạo token mới thành công",
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token,
                }
                return data_response, "SUCCESS"

            return {"message": "Lỗi không xác định khi tạo token mới"}, "SERVER_INTERNAL_ERROR"

        except jwt.ExpiredSignatureError:
            return {"message": "Refresh token đã hết hạn"}, "ERROR_UNAUTHORIZED"

        except Exception as e:
            current_app.logger.error(f"Lỗi làm mới token: {str(e)}", exc_info=True)
            return {"message": "Lỗi không xác định"}, "SERVER_INTERNAL_ERROR"

    def activate_user_account(self, email=None):
        if not email:
            return {"message": "Không có email đâu vào"}, "BAD_REQUEST"

        try:
            is_active = self.user_repository.active_user_by_email(email)
            if is_active:
                return {"message": "Cập nhật trạng thái thành công"}, "SUCCESS"

            return {"message": "Kích hoạt không hợp lệ"}, "ERROR_UNAUTHORIZED"
        except Exception as e:
            current_app.logger.error(f"Có vấn đề khi cập nhật trạng thái user: {str(e)}",
                                     exc_info=True)
            return {"message": "Có vấn đề khi cập nhật trạng thái user"}, "SERVER_INTERNAL_ERROR"

class UserService:
    def __init__(self, user_repository):
        self.user_repository = user_repository

    @staticmethod
    def get_user_data(user=None):
        if not user:
            return None

        user_data = {
            "id": user.id,
            "name": user.username,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "email": user.email,
            "role": user.role.name,
            "createdAt": user.created_date.isoformat(),
            "profile": None,
        }

        if user.profile:
            user_data["profile"] = user.profile.to_dict()

        return user_data

    @handle_db_errors
    def update_patient_profile_service(self, current_user=None, data=None):
        if not current_user:
            return {"message": "Người dùng không tồn tại"}, "FORBIDDEN"

        if "PATIENT" not in current_user.role.name.upper():
            return {"message": "Không có hồ sơ người dùng này"}, "FORBIDDEN"

        profile = current_user.profile
        add_profile_updates(current_user, data, {"firstName": "first_name", "lastName": "last_name"})
        add_profile_updates(profile, data, {"address": "address", "phone": "phone"})
        update_extended_profile(profile, data)

        if data.get("dayOfBirth"):
            parsed_date, err = parse_date(data.get("dayOfBirth"))
            if err:
                return {"message": err}, "ERROR_BAD_REQUEST"
            profile.birthday = parsed_date

        self.user_repository.commit()

        updated_user = self.get_user_data(current_user)
        if updated_user:
            return {"message": "Cập nhật hồ sơ thành công", "data": updated_user}, "SUCCESS"

        return {"message": "Lỗi không xác định khi cập nhật hồ sơ"}, "SERVER_INTERNAL_ERROR"
