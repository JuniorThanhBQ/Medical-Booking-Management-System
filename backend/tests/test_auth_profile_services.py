from unittest.mock import patch

import pytest
from werkzeug.security import generate_password_hash

from src.modules.auth_profile.models import PatientProfile, User, UserRole
from src.modules.auth_profile.services import (check_email_exists_service,
                                               login_google_service,
                                               login_user_service,
                                               register_user_service,
                                               update_patient_profile_service)
from tests.test_base import test_app, test_session


class TestUserLogin:
    @pytest.fixture
    def setup_active_user(self, test_session):
        user = User(
            username="active_user",
            email="active_user@example.com",
            password=generate_password_hash("CorrectPassword123!"),
            first_name="Active",
            last_name="User",
            role=UserRole.PATIENT,
            is_active=True
        )
        test_session.add(user)
        test_session.commit()
        return user

    @pytest.fixture
    def setup_inactive_user(self, test_session):
        user = User(
            username="locked_user",
            email="locked_user@example.com",
            password=generate_password_hash("CorrectPassword123!"),
            first_name="Locked",
            last_name="User",
            role=UserRole.PATIENT,
            is_active=False
        )
        test_session.add(user)
        test_session.commit()
        return user

    def test_successful_login_with_valid_credentials(self, test_session, setup_active_user):
        token, message, user_data, status = login_user_service(
            "active_user@example.com", "CorrectPassword123!"
        )
        assert status == "SUCCESS"
        assert token is not None
        assert message == "Đăng nhập thành công"
        assert user_data["email"] == "active_user@example.com"
        assert user_data["role"] == "PATIENT"

    def test_login_fails_with_incorrect_password(self, test_session, setup_active_user):
        token, message, user_data, status = login_user_service(
            "active_user@example.com", "WrongPassword123!"
        )
        assert status == "ERROR_UNAUTHORIZED"
        assert message == "Tài khoản hoặc mật khẩu không đúng"
        assert token is None
        assert user_data is None

    def test_login_fails_for_inactive_user(self, test_session, setup_inactive_user):
        token, message, user_data, status = login_user_service(
            "locked_user@example.com", "CorrectPassword123!"
        )
        assert status == "FORBIDDEN"
        assert message == "Tài khoản đã bị khóa"
        assert token is None
        assert user_data is None


class TestUserRegistration:
    @patch("src.modules.auth_profile.services.cloudinary_upload_process")
    def test_successful_registration_with_all_valid_fields(self, mock_cloudinary, test_session):
        mock_cloudinary.return_value = "https://cloudinary.com/fake_avatar.jpg"

        payload = {
            "username": "newuser",
            "password": "SecurePassword123!",
            "email": "newuser@example.com",
            "first_name": "New",
            "last_name": "User",
            "avatar": "<base64_data>",
            "birthday": "1990-01-15",
            "gender": "MALE",
            "phone": "1234567890",
            "address": "123 Main St",
            "medical_history": "None"
        }

        user_data, message, status = register_user_service(payload)

        assert status == "SUCCESS"
        assert message == "Đăng ký thành công"
        assert user_data["email"] == "newuser@example.com"
        assert user_data["profile"]["gender"] == "MALE"
        assert "1990-01-15" in user_data["profile"]["dateOfBirth"]

        mock_cloudinary.assert_called_once_with("<base64_data>")

        db_user = User.query.filter_by(email="newuser@example.com").first()
        assert db_user is not None
        assert db_user.profile is not None

    def test_registration_fails_due_to_existing_email(self, test_session):
        existing_user = User(
            username="existing", email="existing@example.com",
            password="pwd", first_name="E", last_name="U"
        )
        test_session.add(existing_user)
        test_session.commit()

        payload = {
            "username": "duplicate_user", "password": "Password123!",
            "email": "existing@example.com", "first_name": "Duplicate", "last_name": "User"
        }

        user_data, message, status = register_user_service(payload)

        assert status == "ERROR_BAD_REQUEST"
        assert message == "Email đã tồn tại"
        assert user_data is None

    def test_registration_fails_due_to_invalid_birthday_format(self, test_session):
        payload = {
            "username": "bad_date_user", "password": "Password123!",
            "email": "baddate@example.com", "birthday": "15/01/1990",
            "first_name": "Bad", "last_name": "Date"
        }

        user_data, message, status = register_user_service(payload)

        assert status == "ERROR_BAD_REQUEST"
        assert message == "Sai định dạng (YYYY-MM-DD)"
        assert user_data is None
        assert User.query.filter_by(email="baddate@example.com").first() is None

    def test_registration_handles_invalid_gender_silently(self, test_session):
        payload = {
            "username": "edge_gender", "password": "Password123!",
            "email": "edge@example.com", "gender": "ALIEN",
            "first_name": "Edge", "last_name": "User"
        }

        user_data, message, status = register_user_service(payload)

        assert status == "SUCCESS"
        assert message == "Đăng ký thành công"
        assert user_data["profile"]["gender"] == "NOT_SET"


class TestGoogleSSOLogin:
    @patch("src.modules.auth_profile.services.verify_google_token")
    def test_successful_login_for_existing_google_user(self, mock_verify, test_session):
        mock_verify.return_value = {"email": "existing@example.com", "name": "Existing User"}
        user = User(username="existing", email="existing@example.com", password="pwd", first_name="E", last_name="U")
        test_session.add(user)
        test_session.commit()

        result, error, status = login_google_service("valid_google_jwt_token")

        assert status == "SUCCESS"
        assert error is None
        assert "token" in result
        assert result["user"]["email"] == "existing@example.com"
        mock_verify.assert_called_once_with("valid_google_jwt_token")

    @patch("src.modules.auth_profile.services.verify_google_token")
    def test_successful_login_and_auto_registration_for_new_google_user(self, mock_verify, test_session):
        mock_verify.return_value = {"email": "newgoogle@example.com", "name": "New Google User"}

        result, error, status = login_google_service("valid_google_jwt_token_new_user")

        assert status == "SUCCESS"
        assert error is None
        assert result["user"]["email"] == "newgoogle@example.com"
        assert result["user"]["firstName"] == "New"

        db_user = User.query.filter_by(email="newgoogle@example.com").first()
        assert db_user is not None

    @patch("src.modules.auth_profile.services.verify_google_token")
    def test_login_fails_with_invalid_google_token(self, mock_verify, test_session):
        mock_verify.return_value = None
        response = login_google_service("invalid_or_expired_token")

        assert len(response) == 2
        assert response[0] is None
        assert response[1] == "Google token không hợp lệ"


class TestUpdatePatientProfile:
    @pytest.fixture
    def setup_patient_with_profile(self, test_session):
        user = User(username="patient", email="patient@ex.com", password="pwd", first_name="P", last_name="T",
                    role=UserRole.PATIENT)
        test_session.add(user)
        test_session.flush()
        profile = PatientProfile(user_id=user.id, phone="111")
        test_session.add(profile)
        test_session.commit()
        return user

    def test_successfully_update_patient_profile_fields(self, test_session, setup_patient_with_profile):
        user = setup_patient_with_profile
        data = {
            "firstName": "UpdatedName",
            "phone": "0987654321",
            "dayOfBirth": "1995-05-05"
        }

        user_data, message, status = update_patient_profile_service(user, data)

        assert status == "SUCCESS"
        assert message == "Cập nhật hồ sơ thành công"
        assert user_data["firstName"] == "UpdatedName"
        assert user_data["profile"]["phone"] == "0987654321"
        assert "1995-05-05" in user_data["profile"]["dateOfBirth"]

    def test_update_fails_for_non_patient_role(self, test_session):
        doctor_user = User(username="doc", email="doc@ex.com", password="pwd", first_name="D", last_name="C",
                           role=UserRole.DOCTOR)

        user_data, message, status = update_patient_profile_service(doctor_user, {"firstName": "DoctorName"})

        assert status == "FORBIDDEN"
        assert message == "Chỉ có bệnh nhân mới được phép cập nhật hồ sơ tại đây"

    def test_update_fails_if_profile_is_missing(self, test_session):
        patient_no_profile = User(username="nop", email="nop@ex.com", password="pwd", first_name="N", last_name="P",
                                  role=UserRole.PATIENT)

        user_data, message, status = update_patient_profile_service(patient_no_profile, {"address": "New Address"})

        assert status == "ERROR_BAD_REQUEST"
        assert message == "Hồ sơ không tồn tại."

    def test_update_ignores_invalid_gender_silently(self, test_session, setup_patient_with_profile):
        user = setup_patient_with_profile
        data = {
            "gender": "UNKNOWN_GENDER",
            "firstName": "ValidName"
        }

        user_data, message, status = update_patient_profile_service(user, data)

        assert status == "SUCCESS"
        assert user_data["firstName"] == "ValidName"


class TestCheckEmailExistence:
    def test_email_is_available(self, test_session):
        result = check_email_exists_service("not_in_db@example.com")
        assert result is True

    def test_email_is_already_taken(self, test_session):
        user = User(username="taken", email="existing@example.com", password="pwd", first_name="T", last_name="K")
        test_session.add(user)
        test_session.commit()

        result = check_email_exists_service("existing@example.com")
        assert result is False
