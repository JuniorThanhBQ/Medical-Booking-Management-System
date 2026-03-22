import datetime

import jwt
from flask import current_app
from werkzeug.security import check_password_hash, generate_password_hash

from src.extensions import db
from src.utils.decorator import handle_db_errors
from src.modules.auth_profile.models import GenderRole, PatientProfile, User
from src.utils.utils import cloudinary_upload_process, verify_google_token


def get_user_loader(user_id):
    return db.session.get(User, int(user_id))


def create_token(user):
    user_payload = {
        "user_id": user.id,
        "role": user.role.name,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=12),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }

    secret_key = current_app.config.get("SECRET_KEY")
    token = jwt.encode(user_payload, secret_key, algorithm="HS256")
    return token


def get_user_data(user):
    user_data = {
        "id": user.id,
        "name": user.username,
        "firstName": user.first_name,
        "lastName": user.last_name,
        "email": user.email,
        "role": user.role.name if user.role else None,
        "createdAt": user.created_date.isoformat() if user.created_date else None,
        "profile": None,
    }

    if user.profile:
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

@handle_db_errors(parameter=4)
def login_user_service(login_email, password):
    user = User.query.filter(User.email == login_email).first()

    if not user or not check_password_hash(user.password, password):
        return None, "Tài khoản hoặc mật khẩu không đúng", None, "ERROR_UNAUTHORIZED"

    if not user.is_active:
        return None, "Tài khoản đã bị khóa", None, "FORBIDDEN"

    token = create_token(user)
    user_data = get_user_data(user)

    return token, "Đăng nhập thành công", user_data, "SUCCESS"

@handle_db_errors(parameter=3)
def register_user_service(user_payload):
    username = user_payload.get("username")
    password = user_payload.get("password")
    email = user_payload.get("email")
    first_name = user_payload.get("first_name")
    last_name = user_payload.get("last_name")
    avatar = user_payload.get("avatar")
    birthday = user_payload.get("birthday")
    gender = user_payload.get("gender")
    phone = user_payload.get("phone")
    address = user_payload.get("address")
    medical_history = user_payload.get("medical_history")

    if User.query.filter_by(username=username).first():
        return None, "Username đã tồn tại", "ERROR_BAD_REQUEST"

    if User.query.filter_by(email=email).first():
        return None, "Email đã tồn tại", "ERROR_BAD_REQUEST"

    new_user = User(
        username=username,
        password=generate_password_hash(password),
        email=email,
        first_name=first_name,
        last_name=last_name,
    )
    db.session.add(new_user)
    db.session.flush()

    avatar_url = None
    if avatar:
        avatar_url = cloudinary_upload_process(avatar)

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
            db.session.rollback()
            return None, "Sai định dạng (YYYY-MM-DD)", "ERROR_BAD_REQUEST"

    new_profile = PatientProfile(
        user_id=new_user.id,
        phone=phone,
        avatar=avatar_url,
        gender=set_gender,
        birthday=set_birthday,
        address=address,
        medical_history=medical_history,
    )
    db.session.add(new_profile)
    db.session.commit()

    return get_user_data(new_user), "Đăng ký thành công", "SUCCESS"

@handle_db_errors(parameter=3)
def login_google_service(google_token):
    user_info = verify_google_token(google_token)

    if not user_info:
        return None, "Google token không hợp lệ"

    email = user_info.get("email")
    name = user_info.get("name", "")
    user = User.query.filter_by(email=email).first()

    if not user:
        parts = name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        user = User(
            username=email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=generate_password_hash("google_sso_random_pass_xyz"),
            role="PATIENT",
        )
        db.session.add(user)
        db.session.commit()

    user_data = get_user_data(user)
    token = create_token(user)

    return {"token": token, "user": user_data}, None, "SUCCESS"

@handle_db_errors(parameter=3)
def update_patient_profile_service(current_user, data):
    user_role = current_user.role.name

    if "PATIENT" not in user_role.upper():
        return None, "Chỉ có bệnh nhân mới được phép cập nhật hồ sơ tại đây", "FORBIDDEN"

    if not current_user.profile:
        return None, "Hồ sơ không tồn tại.", "ERROR_BAD_REQUEST"

    if "firstName" in data:
        current_user.first_name = data["firstName"]

    if "lastName" in data:
        current_user.last_name = data["lastName"]

    profile = current_user.profile

    if "address" in data:
        profile.address = data["address"]

    if "phone" in data:
        profile.phone = data["phone"]

    if "avatar" in data:
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
            return None, "Vui lòng định dạng theo YYYY-mm-dd", "ERROR_BAD_REQUEST"

    db.session.commit()
    return get_user_data(current_user), "Cập nhật hồ sơ thành công", "SUCCESS"
