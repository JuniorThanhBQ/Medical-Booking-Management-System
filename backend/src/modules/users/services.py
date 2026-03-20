import datetime
import logging
from functools import wraps

import cloudinary.uploader
import jwt
from flask import current_app, request
from werkzeug.security import check_password_hash, generate_password_hash

from src.modules.users.models import GenderRole, PatientProfile, User, db
from src.utils.utils import cloudinary_upload_process, verify_google_token


def get_user_loader(user_id):
    return db.session.get(User, int(user_id))


def register_user_service(
    username, password, email, first_name, last_name, avatar, birthday, gender, phone
):
    if User.query.filter_by(username=username).first():
        return None, "Username đã tồn tại", "ERROR_BAD_REQUEST"

    if User.query.filter_by(email=email).first():
        return None, "Email đã tồn tại", "ERROR_BAD_REQUEST"

    try:
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

        parsed_gender = GenderRole.NOT_SET
        if gender:
            try:
                parsed_gender = GenderRole[gender.upper()]
            except KeyError:
                pass

        parsed_birthday = None
        if birthday:
            try:
                parsed_birthday = datetime.datetime.strptime(birthday, "%Y-%m-%d")
            except ValueError:
                db.session.rollback()
                return None, "Sai định dạng ngày sinh (YYYY-MM-DD)", "ERROR_BAD_REQUEST"

        new_profile = PatientProfile(
            user_id=new_user.id,
            phone=phone,
            avatar=avatar_url,
            gender=parsed_gender,
            birthday=parsed_birthday,
        )
        db.session.add(new_profile)
        db.session.commit()
        user_data = get_user_information(new_user)

        return user_data, "Đăng ký thành công", "SUCCESS"

    except Exception as ex:
        db.session.rollback()
        logging.error(f"Có lỗi xảy ra khi thực hiện đăng ký: {str(ex)}")
        return None, "Có lỗi xảy ra trong quá trình đăng ký!", "SERVER_INTERNAL_ERROR"


def create_token(user):
    payload = {
        "user_id": user.id,
        "role": user.role.name,
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(hours=8),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }

    secret_key = current_app.config.get("SECRET_KEY") or ("fake-key" * 5)
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def login_user_service(login_email, password):
    user = User.query.filter(User.email == login_email).first()

    if not user or not (check_password_hash(user.password, password)):
        return None, "Tài khoản hoặc mật khẩu có thể không đúng", "ERROR_UNAUTHORIZED"

    if not user.is_active:
        return None, "Tài khoản đã bị khóa", "FORBIDDEN"

    token = create_token(user)
    return token, "Đăng nhập thành công", "SUCCESS"


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return {"message": "Có vấn đề trong xác thực token"}, 401
        try:
            token_val = token.split(" ")[1]
            secret_key = current_app.config.get("SECRET_KEY") or ("fake-key" * 5)
            data = jwt.decode(token_val, secret_key, algorithms=["HS256"])
            current_user = db.session.get(User, data["user_id"])

            if not current_user:
                return {"message": "User không tồn tại"}, 401

        except jwt.ExpiredSignatureError:
            return {"message": "Token đã hết hạn"}, 401
        except jwt.InvalidTokenError:
            return {"message": "Token không hợp lệ"}, 401

        return f(current_user, *args, **kwargs)

    return decorator


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

    user_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role.name if getattr(user, "role", None) else None,
    }

    token = create_token(user)
    return {"token": token, "user": user_data}, None


def get_user_information(current_user):
    user_data = {
        "username": current_user.username,
        "first_name": current_user.first_name,
        "last_name": current_user.last_name,
        "email": current_user.email,
        "role": current_user.role.name,
        "created_date": (
            current_user.created_date.isoformat() if current_user.created_date else None
        ),
        "updated_date": (
            current_user.updated_date.isoformat() if current_user.updated_date else None
        ),
    }

    profile = current_user.profile
    if profile:
        profile_data = {
            "profile_type": profile.profile_type,
            "address": profile.address,
            "birthday": (
                profile.birthday.strftime("%Y-%m-%d") if profile.birthday else None
            ),
            "phone": profile.phone,
            "gender": profile.gender.name,
            "avatar": profile.avatar,
        }

        if profile.profile_type == "doctor":
            profile_data.update(
                {
                    "about": getattr(profile, "about", None),
                    "year_of_experience": getattr(profile, "year_of_experience", None),
                    "specialty": profile.specialty.name if profile.specialty else None,
                    "work_schedule": (
                        profile.work_schedule.title if profile.work_schedule else None
                    ),
                }
            )
        elif profile.profile_type == "patient":
            profile_data.update(
                {"medical_history": getattr(profile, "medical_history", None)}
            )

        user_data["profile"] = profile_data
    else:
        user_data["profile"] = None

    return user_data


def update_patient_profile_service(current_user, data):
    user_role = current_user.role.name

    if "PATIENT" not in user_role.upper():
        return (
            None,
            "Chỉ có bệnh nhân mới được phép cập nhật hồ sơ tại đây",
            "FORBIDDEN",
        )

    if not current_user.profile:
        return None, "Hồ sơ chưa tồn tại, vui lòng tạo hồ sơ", "ERROR_BAD_REQUEST"

    try:
        if "first_name" in data:
            current_user.first_name = data["first_name"]

        if "last_name" in data:
            current_user.last_name = data["last_name"]

        profile = current_user.profile

        if "address" in data:
            profile.address = data["address"]

        if "phone" in data:
            profile.phone = data["phone"]

        avatar_url = None
        if "avatar" in data:
            avatar_url = cloudinary_upload_process(data["avatar"])
            profile.avatar = avatar_url

        if "medical_history" in data and profile.profile_type == "patient":
            profile.medical_history = data["medical_history"]

        if data.get("gender"):
            try:
                profile.gender = GenderRole[data.get("gender").upper()]
            except KeyError:
                pass

        if data.get("birthday"):
            try:
                profile.birthday = datetime.datetime.strptime(
                    data.get("birthday"), "%Y-%m-%d"
                )
            except ValueError:
                return None, "Vui lòng định dạng theo YYYY-mm-dd", "ERROR_BAD_REQUEST"

        db.session.commit()
        return (
            get_user_information(current_user),
            "Cập nhật hồ sơ thành công",
            "SUCCESS",
        )

    except Exception as ex:
        db.session.rollback()
        logging.error(f"Lỗi cập nhật profile: {str(ex)}")
        return None, "Có lỗi xảy ra khi cập nhật hồ sơ!", "SERVER_INTERNAL_ERROR"
