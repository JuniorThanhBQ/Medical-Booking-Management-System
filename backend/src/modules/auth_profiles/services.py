import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from src.extensions import db
from src.modules.auth_profiles.models import GenderRole, PatientProfile, User
from src.utils.handle_db_errors import handle_db_errors
from src.utils.utils import cloudinary_upload_process, create_token


def get_user_data(user):
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
                    {"id": profile.specialty.id,
                     "name": profile.specialty.name
                     } if profile.specialty else None
                ),
            })
        elif profile.profile_type == "patient":
            profile_data.update(
                {"medicalHistory": profile.medical_history}
            )

        user_data["profile"] = profile_data

    return user_data


@handle_db_errors
def login_user_service(login_email, password, role):
    user = User.query.filter(User.email == login_email).first()

    if not user or not check_password_hash(user.password, password):
        return None, None, "ERROR_UNAUTHORIZED"

    if not user.is_active:
        return None, None, "FORBIDDEN"

    if role.upper() != user.role.name:
        return None, None, "FORBIDDEN"

    token = create_token(user)
    user_data = get_user_data(user)

    return token, user_data, "SUCCESS"


@handle_db_errors
def register_user_service(user_payload):
    email = user_payload.get("email")
    avatar = user_payload.get("avatar")
    birthday = user_payload.get("birthday")
    gender = user_payload.get("gender")
    phone = user_payload.get("phone")
    address = user_payload.get("address")
    medical_history = user_payload.get("medical_history")

    if User.query.filter_by(email=email).first():
        return None, "ERROR_BAD_REQUEST"

    new_user = User(
        username=user_payload.get("username"),
        password=generate_password_hash(user_payload.get("password")),
        email=email,
        first_name=user_payload.get("first_name"),
        last_name=user_payload.get("last_name"),
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
            return None, "ERROR_BAD_REQUEST"

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

    return get_user_data(new_user), "SUCCESS"


def check_email_exists_service(email: str):
    user = User.query.filter_by(email=email).first()

    if user:
        return False

    return True


@handle_db_errors
def update_patient_profile_service(current_user, data):
    user_role = current_user.role.name

    if "PATIENT" not in user_role.upper():
        return None, "FORBIDDEN"

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
            return None, "ERROR_BAD_REQUEST"

    db.session.commit()
    return get_user_data(current_user), "SUCCESS"
