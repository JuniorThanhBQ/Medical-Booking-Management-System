from unittest.mock import patch

import jwt
import pytest
from flask import current_app
from werkzeug.security import generate_password_hash

from src.modules.auth_profiles.models import (DoctorProfile, GenderRole,
                                              PatientProfile, Specialty, User,
                                              UserRole)
from src.modules.auth_profiles.services import (check_email_exists_service,
                                                get_user_data,
                                                login_user_service,
                                                register_user_service,
                                                update_patient_profile_service)
from src.utils.utils import cloudinary_upload_process, create_token
from tests.test_base import test_app, test_session


@pytest.fixture
def base_patient(test_session):
    user = User(
        username="patient_test",
        password=generate_password_hash("pass123"),
        email="patient@example.com",
        first_name="John",
        last_name="Doe",
        is_active=True
    )
    user.role = UserRole.PATIENT
    test_session.add(user)
    test_session.commit()

    profile = PatientProfile(
        user_id=user.id,
        phone="0123456789",
        gender=GenderRole.MALE,
        medical_history="None"
    )
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def base_doctor(test_session):
    user = User(
        username="doctor_test",
        password=generate_password_hash("pass123"),
        email="doctor@example.com",
        first_name="Jane",
        last_name="Smith",
        is_active=True
    )
    user.role = UserRole.DOCTOR
    test_session.add(user)
    test_session.commit()

    specialty = Specialty(name="Cardiology", level="1")
    test_session.add(specialty)
    test_session.commit()

    profile = DoctorProfile(
        user_id=user.id,
        phone="0987654321",
        gender=GenderRole.FEMALE,
        title="Dr.",
        bio="Expert",
        specialty_id=specialty.id
    )
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def base_payload():
    return {
        "username": "new_user",
        "password": "new_password",
        "email": "new@example.com",
        "first_name": "New",
        "last_name": "User",
        "phone": "111222333",
        "gender": "MALE",
        "birthday": "1990-01-01",
        "address": "123 Street",
        "medical_history": "Healthy"
    }


class TestUtils:
    def test_create_token(self, test_app, base_patient):
        with test_app.app_context():
            token = create_token(base_patient)
            assert isinstance(token, str)

            secret = current_app.config.get("SECRET_KEY")
            decoded = jwt.decode(token, secret, algorithms=["HS256"])

            assert decoded["user_id"] == base_patient.id
            assert decoded["role"] == "PATIENT"
            assert "exp" in decoded
            assert "iat" in decoded

    @patch("src.utils.utils.cloudinary.uploader.upload")
    def test_cloudinary_upload(self, mock_upload):
        mock_upload.return_value = {"secure_url": "https://fake.url/img.png"}
        result = cloudinary_upload_process("fake_file_path")

        mock_upload.assert_called_once_with("fake_file_path")
        assert result == "https://fake.url/img.png"


class TestGetUserData:
    def test_get_no_profile(self, test_session):
        user = User(
            username="noprofile",
            email="no@test.com",
            first_name="No",
            last_name="Profile",
            password=generate_password_hash("Admin123@")
        )
        user.role = UserRole.PATIENT
        test_session.add(user)
        test_session.commit()

        result = get_user_data(user)
        assert result["id"] == user.id
        assert result["profile"] is None

    def test_get_patient_profile(self, base_patient):
        result = get_user_data(base_patient)
        assert result["profile"]["gender"] == "MALE"
        assert result["profile"]["medicalHistory"] == "None"
        assert "specialty" not in result["profile"]

    def test_get_doctor_profile(self, base_doctor):
        result = get_user_data(base_doctor)
        assert result["profile"]["title"] == "Dr."
        assert result["profile"]["bio"] == "Expert"
        assert result["profile"]["specialty"]["name"] == "Cardiology"


class TestLoginService:
    def test_login_success(self, test_app, base_patient):
        with test_app.app_context():
            token, data, msg = login_user_service("patient@example.com",
                                                  "pass123", "PATIENT")
            assert msg == "SUCCESS"
            assert data["email"] == "patient@example.com"
            assert token is not None

    def test_login_wrong_password(self, test_app, base_patient):
        with test_app.app_context():
            token, data, msg = login_user_service("patient@example.com",
                                                  "wrongpass", "PATIENT")
            assert msg == "ERROR_UNAUTHORIZED"
            assert token is None

    def test_login_wrong_role(self, test_app, base_patient):
        with test_app.app_context():
            token, data, msg = login_user_service("patient@example.com",
                                                  "pass123", "DOCTOR")
            assert msg == "FORBIDDEN"
            assert token is None

    def test_login_inactive(self, test_app, test_session, base_patient):
        base_patient.is_active = False
        test_session.commit()
        with test_app.app_context():
            token, data, msg = login_user_service("patient@example.com",
                                                  "pass123", "PATIENT")
            assert msg == "FORBIDDEN"
            assert token is None


class TestRegisterService:
    @patch("src.modules.auth_profiles.services.cloudinary_upload_process")
    def test_register_success(self, mock_upload, test_app, base_payload):
        mock_upload.return_value = "https://fake.url/avatar.png"
        base_payload["avatar"] = "fake_file"

        with test_app.app_context():
            data, msg = register_user_service(base_payload)

            assert msg == "SUCCESS"
            assert data["email"] == "new@example.com"
            assert data["profile"]["avatar"] == "https://fake.url/avatar.png"
            assert data["profile"]["medicalHistory"] == "Healthy"

    def test_register_exist_email(self, test_app, base_payload, base_patient):
        base_payload["email"] = "patient@example.com"
        with test_app.app_context():
            data, msg = register_user_service(base_payload)
            assert msg == "ERROR_BAD_REQUEST"
            assert data is None

    def test_register_bad_date(self, test_app, base_payload):
        base_payload["birthday"] = "invalid-date-format"
        with test_app.app_context():
            data, msg = register_user_service(base_payload)
            assert msg == "ERROR_BAD_REQUEST"
            assert data is None

    def test_register_no_avatar(self, test_app, base_payload):
        base_payload.pop("avatar", None)
        base_payload.pop("gender", None)
        with test_app.app_context():
            data, msg = register_user_service(base_payload)
            assert msg == "SUCCESS"
            assert data["profile"]["avatar"] is None
            assert data["profile"]["gender"] == "NOT_SET"


class TestEmailExistsService:
    def test_email_exists_true(self, test_app, base_patient):
        with test_app.app_context():
            result = check_email_exists_service("patient@example.com")
            assert result is False

    def test_email_exists_false(self, test_app):
        with test_app.app_context():
            result = check_email_exists_service("notfound@example.com")
            assert result is True


class TestUpdateProfileService:
    @patch("src.modules.auth_profiles.services.cloudinary_upload_process")
    def test_update_patient_success(self, mock_upload, test_app, base_patient):
        mock_upload.return_value = "https://fake.url/new.png"
        update_data = {
            "firstName": "Updated",
            "phone": "999888777",
            "avatar": "new_file"
        }
        with test_app.app_context():
            data, msg = update_patient_profile_service(base_patient, update_data)
            assert msg == "SUCCESS"
            assert data["firstName"] == "Updated"
            assert data["profile"]["phone"] == "999888777"
            assert data["profile"]["avatar"] == "https://fake.url/new.png"

    def test_update_wrong_role(self, test_app, base_doctor):
        update_data = {"firstName": "Hacker"}
        with test_app.app_context():
            data, msg = update_patient_profile_service(base_doctor, update_data)
            assert msg == "FORBIDDEN"
            assert data is None

    def test_update_bad_date(self, test_app, base_patient):
        update_data = {"dayOfBirth": "wrong-format"}
        with test_app.app_context():
            data, msg = update_patient_profile_service(base_patient, update_data)
            assert msg == "ERROR_BAD_REQUEST"
            assert data is None
