import datetime

import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from src.libs.cloudinary import cloudinary_upload_process
from src.modules.users.models import GenderRole, PatientProfile, User
from src.modules.users.repositories import (add_profile, add_user, commit,
                                            get_user_by_email)
from src.utils.handle_db_errors import handle_db_errors


def parse_date(date_str):
    if not date_str:
        return None, None
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d"), None
    except ValueError:
        return None, "Sai định dạng ngày sinh"


def parse_gender(gender_str, default: GenderRole = GenderRole.NOT_SET):
    if not gender_str:
        return default
    try:
        return GenderRole[gender_str.upper()]
    except KeyError:
        return default


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

    if not user.profile:
        return user_data

    profile = user.profile
    profile_data = {
        "id": profile.id,
        "address": profile.address,
        "dateOfBirth": profile.birthday.isoformat() if profile.birthday else None,
        "phone": profile.phone,
        "gender": profile.gender.name if profile.gender else None,
        "avatar": profile.avatar,
    }

    if profile.profile_type == "doctor":
        profile_data.update({
            "title": profile.title,
            "bio": profile.bio,
            "specialty": (
                {"id": profile.specialty.id, "name": profile.specialty.name}
                if profile.specialty else None
            ),
        })
    elif profile.profile_type == "patient":
        profile_data.update({"medicalHistory": profile.medical_history})

    user_data["profile"] = profile_data
    return user_data


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
    if get_user_by_email(email):
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
    )
    add_user(new_user)

    new_profile = PatientProfile(
        user_id=new_user.id,
        phone=user_payload.get("phone"),
        avatar=avatar_url,
        gender=set_gender,
        birthday=set_birthday,
        address=user_payload.get("address"),
        medical_history=user_payload.get("medical_history"),
    )
    add_profile(new_profile)
    commit()

    registered_user = get_user_data(new_user)
    if registered_user:
        return {"message": "Đăng ký thành công", "user": registered_user}, "SUCCESS"

    return {"message": "Lỗi không xác định khi đăng kí"}, "SERVER_INTERNAL_ERROR"


def is_email_available(email: str):
    return not bool(get_user_by_email(email))


def apply_updates(obj, data, mapping):
    for payload_key, attr in mapping.items():
        if payload_key in data:
            setattr(obj, attr, data[payload_key])


def update_extended_profile(profile, data):
    if "medicalHistory" in data and profile.profile_type == "patient":
        profile.medical_history = data["medicalHistory"]

    if data.get("avatar"):
        profile.avatar = cloudinary_upload_process(data["avatar"])

    if "gender" in data:
        profile.gender = parse_gender(data.get("gender"), default=profile.gender)


@handle_db_errors
def update_patient_profile_service(current_user=None, data=None):
    if not current_user:
        return {"message": "Người dùng không tồn tại"}, "FORBIDDEN"

    if "PATIENT" not in current_user.role.name.upper():
        return {"message": "Không có hồ sơ người dùng này"}, "FORBIDDEN"

    apply_updates(current_user, data, {"firstName": "first_name", "lastName": "last_name"})
    profile = current_user.profile
    apply_updates(profile, data, {"address": "address", "phone": "phone"})
    update_extended_profile(profile, data)

    if data.get("dayOfBirth"):
        parsed_date, err = parse_date(data.get("dayOfBirth"))
        if err:
            return {"message": err}, "ERROR_BAD_REQUEST"
        profile.birthday = parsed_date

    commit()

    updated_user = get_user_data(current_user)
    if updated_user:
        return {"message": "Cập nhật hồ sơ thành công", "data": updated_user}, "SUCCESS"

    return {"message": "Lỗi không xác định khi cập nhật hồ sơ"}, "SERVER_INTERNAL_ERROR"
