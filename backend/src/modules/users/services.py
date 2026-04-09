import datetime

import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from src.libs.cloudinary import cloudinary_upload_process
from src.modules.users.models import GenderRole, PatientProfile, User
from src.modules.users.repositories import (add_profile, add_user, commit,
                                            get_user_by_email, rollback)
from src.utils.handle_db_errors import handle_db_errors


def create_token(user=None):
    if user:
        user_payload = {
            "user_id": user.id,
            "role": user.role.name,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=12),
            "iat": datetime.datetime.now(datetime.timezone.utc),
        }

        secret_key = current_app.config.get("SECRET_KEY")
        token = jwt.encode(user_payload, secret_key, algorithm="HS256")
        return token

    return None


def get_user_data(user=None):
    if user:
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
            profile = user.profile
            profile_data = {
                "id": profile.id,
                "address": profile.address,
                "dateOfBirth": profile.birthday.isoformat() if profile.birthday else None,
                "phone": profile.phone,
                "gender": profile.gender.name,
                "avatar": profile.avatar,
            }

            if profile.profile_type == "doctor":
                profile_data.update({
                    "title": profile.title,
                    "bio": profile.bio,
                    "specialty": (
                        {"id": profile.specialty.id, "name": profile.specialty.name
                         } if profile.specialty else None
                    ),
                })
            elif profile.profile_type == "patient":
                profile_data.update({"medicalHistory": profile.medical_history})

            user_data["profile"] = profile_data

        return user_data

    return None


@handle_db_errors
def login_user_service(login_email=None, password=None, role=None):
    user = get_user_by_email(login_email)

    if not user or not check_password_hash(user.password, password):
        return {"message": "Sai tên đăng nhập hoặc mật khẩu"}, "ERROR_UNAUTHORIZED"

    if not user.is_active:
        return {"message": "Tài khoản bị khoá"}, "FORBIDDEN"

    if role.upper() != user.role.name:
        return {"message": "Tài khoản không có thẩm quyền truy cập"}, "FORBIDDEN"

    token = create_token(user=user)
    user_data = get_user_data(user=user)

    if token and user_data:
        data = {
            "message": "Đăng nhập thành công",
            "access_token": token,
            "user": user_data,
        }
        return data, "SUCCESS"

    return {"message": "Lỗi không xác định khi đăng nhập"}, "SERVER_INTERNAL_ERROR"


@handle_db_errors
def register_user_service(user_payload=None):
    if not user_payload:
        return None, "ERROR_BAD_REQUEST"

    email = user_payload.get("email")
    avatar = user_payload.get("avatar")
    birthday = user_payload.get("birthday")
    gender = user_payload.get("gender")
    phone = user_payload.get("phone")
    address = user_payload.get("address")
    medical_history = user_payload.get("medical_history")

    if get_user_by_email(email):
        return {"message": "Email đã tồn tại"}, "ERROR_BAD_REQUEST"

    avatar_url = None
    if avatar:
        avatar_url = cloudinary_upload_process(avatar)

    new_user = User(
        username=user_payload.get("username"),
        password=generate_password_hash(user_payload.get("password")),
        email=email,
        first_name=user_payload.get("first_name"),
        last_name=user_payload.get("last_name"),
    )
    add_user(new_user)

    set_gender = GenderRole.NOT_SET
    if gender:
        try:
            set_gender = GenderRole[gender.upper()]
        except KeyError:
            pass

    set_birthday = None
    if birthday:
        try:
            set_birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            rollback()
            return {"message": "Sai định dạng ngày sinh"}, "ERROR_BAD_REQUEST"

    new_profile = PatientProfile(
        user_id=new_user.id,
        phone=phone,
        avatar=avatar_url,
        gender=set_gender,
        birthday=set_birthday,
        address=address,
        medical_history=medical_history,
    )
    add_profile(new_profile)
    commit()

    registered_user = get_user_data(new_user)
    if registered_user:
        data = {
            "message": "Đăng ký thành công",
            "user": registered_user,
        }

        return data, "SUCCESS"

    return {"message": "Lỗi không xác định khi đăng kí"}, "SERVER_INTERNAL_ERROR"


def is_email_available(email: str):
    user = get_user_by_email(email)

    if user:
        return False

    return True


@handle_db_errors
def update_patient_profile_service(current_user=None, data=None):
    if not current_user:
        return {"message": "Người dùng không tồn tại"}, "FORBIDDEN"

    user_role = current_user.role.name

    if "PATIENT" not in user_role.upper():
        return {"message": "Không có hồ sơ người dùng này"}, "FORBIDDEN"

    if "firstName" in data:
        current_user.first_name = data["firstName"]

    if "lastName" in data:
        current_user.last_name = data["lastName"]

    profile = current_user.profile
    if "address" in data:
        profile.address = data["address"]

    if "phone" in data:
        profile.phone = data["phone"]

    if data.get("avatar"):
        avatar_url = cloudinary_upload_process(data["avatar"])
        profile.avatar = avatar_url

    if "medicalHistory" in data and profile.profile_type == "patient":
        profile.medical_history = data["medicalHistory"]

    if data.get("gender"):
        try:
            profile.gender = GenderRole[data.get("gender").upper()]
        except KeyError:
            pass

    if data.get("dayOfBirth"):
        try:
            profile.birthday = datetime.datetime.strptime(data.get("dayOfBirth"), "%Y-%m-%d")
        except ValueError:
            return {"message": "Định dạng ngày sinh không phù hợp"}, "ERROR_BAD_REQUEST"

    commit()

    updated_user = get_user_data(current_user)
    if updated_user:
        data = {
            "message": "Cập nhật hồ sơ thành công",
            "data": updated_user,
        }

        return data, "SUCCESS"

    return {"message": "Lỗi không xác định khi cập nhật hồ sơ"}, "SERVER_INTERNAL_ERROR"
