from unittest.mock import patch

from werkzeug.security import generate_password_hash

from src.modules.users.models import GenderRole, PatientProfile, User, UserRole
from src.modules.users.repositories import add_profile, add_user, commit
from src.modules.users.services import (create_token, get_user_data,
                                        is_email_available, login_user_service,
                                        parse_date, parse_gender,
                                        register_user_service,
                                        update_patient_profile_service)
from tests.test_base import test_app, test_session


def setup_dummy_user(email="service@test.com", role=UserRole.PATIENT, is_active=True):
    user = User(
        username="service_user",
        password=generate_password_hash("password123"),
        email=email,
        first_name="Service",
        last_name="User",
        role=role,
        is_active=is_active
    )
    add_user(user)
    profile = PatientProfile(user_id=user.id, phone="0987654321")
    add_profile(profile)
    commit()
    return user

def test_parse_helpers():
    assert parse_date(None) == (None, None)
    date_obj, err = parse_date("2000-01-01")
    assert date_obj.year == 2000 and err is None
    date_obj, err = parse_date("invalid-date")
    assert err == "Sai định dạng ngày sinh"
    assert parse_gender(None) == GenderRole.NOT_SET
    assert parse_gender("male") == GenderRole.MALE
    assert parse_gender("unknown") == GenderRole.NOT_SET

def test_create_token(test_app):
    with test_app.app_context():
        user = setup_dummy_user(email="token@test.com")
        token = create_token(user)
        assert token is not None
        assert isinstance(token, str)

def test_get_user_data(test_app, test_session):
    with test_app.app_context():
        assert get_user_data(None) is None
        user = setup_dummy_user(email="data@test.com")
        data = get_user_data(user)
        assert data["email"] == "data@test.com"
        assert data["profile"]["phone"] == "0987654321"

def test_login_user_service(test_app, test_session):
    with test_app.app_context():
        setup_dummy_user(email="login@test.com", role=UserRole.PATIENT)
        setup_dummy_user(email="locked@test.com", is_active=False)

        res, code = login_user_service("wrong@test.com", "pwd", "PATIENT")
        assert code == "ERROR_UNAUTHORIZED"

        res, code = login_user_service("login@test.com", "wrong_pwd", "PATIENT")
        assert code == "ERROR_UNAUTHORIZED"

        res, code = login_user_service("locked@test.com", "password123", "PATIENT")
        assert code == "FORBIDDEN"

        res, code = login_user_service("login@test.com", "password123", "DOCTOR")
        assert code == "FORBIDDEN"

        res, code = login_user_service("login@test.com", "password123", "PATIENT")
        assert code == "SUCCESS"
        assert "access_token" in res
        assert "refresh_token" in res


@patch('src.modules.users.services.cloudinary_upload_process', return_value="http://cloudinary.com/new.png")
def test_update_patient_profile_service(mock_cloudinary, test_app, test_session):
    with test_app.app_context():
        user = setup_dummy_user(email="update@test.com")
        doctor = setup_dummy_user(email="doctor@test.com", role=UserRole.DOCTOR)

        res, code = update_patient_profile_service(None, {})
        assert code == "FORBIDDEN"

        res, code = update_patient_profile_service(doctor, {})
        assert code == "FORBIDDEN"

        payload = {
            "firstName": "Updated", "address": "New Address",
            "avatar": "newimg", "gender": "female", "dayOfBirth": "1995-05-05"
        }
        res, code = update_patient_profile_service(user, payload)
        assert code == "SUCCESS"
        assert user.first_name == "Updated"
        assert user.profile.address == "New Address"
        assert user.profile.gender == GenderRole.FEMALE