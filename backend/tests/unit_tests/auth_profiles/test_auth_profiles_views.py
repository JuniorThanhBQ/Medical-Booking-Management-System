from unittest.mock import patch

import pytest
from flask_restx import Api

from src.extensions import limiter
from src.modules.auth_profiles.models import User, UserRole
from src.modules.auth_profiles.views import auth_namespace
from src.utils.utils import create_token
from tests.test_base import test_app, test_session


@pytest.fixture
def configured_client(test_app):
    if hasattr(auth_namespace, 'apis'):
        auth_namespace.apis.clear()

    api = Api(test_app)
    limiter.init_app(test_app)
    api.add_namespace(auth_namespace, path="/auth")

    return test_app.test_client()


@pytest.fixture
def mock_user(test_session):
    user = User(
        username="testuser",
        password="hashed",
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    user.role = UserRole.PATIENT
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def valid_header(mock_user, test_app):
    with test_app.app_context():
        token = create_token(mock_user)
    return {"Authorization": f"Bearer {token}"}


class TestLoginAPI:
    @patch("src.modules.auth_profiles.views.login_user_service")
    def test_login_success(self, mock_service, configured_client):
        mock_service.return_value = ("fake_token", {"id": 1}, "SUCCESS")
        payload = {"email": "test@example.com", "password": "Password123@", "role": "PATIENT"}
        response = configured_client.post("/auth/login", json=payload)
        assert response.status_code == 200
        assert response.json["message"] == "Đăng nhập thành công"

    def test_login_missing_fields(self, configured_client):
        payload = {"email": "test@example.com"}
        response = configured_client.post("/auth/login", json=payload)
        assert response.status_code == 400

    def test_login_invalid_format(self, configured_client):
        payload = {"email": "invalid_email", "password": "123", "role": "PATIENT"}
        response = configured_client.post("/auth/login", json=payload)
        assert response.status_code == 400

    @patch("src.modules.auth_profiles.views.login_user_service")
    def test_login_unauthorized(self, mock_service, configured_client):
        mock_service.return_value = (None, None, "ERROR_UNAUTHORIZED")
        payload = {"email": "test@example.com", "password": "Password123@", "role": "PATIENT"}
        response = configured_client.post("/auth/login", json=payload)
        assert response.status_code == 401

    def test_login_rate_limit(self, configured_client):
        payload = {"email": "test@example.com", "password": "Password123@", "role": "PATIENT"}
        for _ in range(50):
            configured_client.post("/auth/login", json=payload)
        response = configured_client.post("/auth/login", json=payload)
        assert response.status_code == 429

    @patch("src.modules.auth_profiles.views.login_user_service")
    def test_login_forbidden_error(self, mock_service, configured_client):
        mock_service.return_value = (None, None, "FORBIDDEN")
        payload = {"email": "test@example.com", "password": "Password123@", "role": "ADMIN"}
        response = configured_client.post("/auth/login", json=payload)
        assert response.status_code == 403
        assert response.json["message"] == "Tài khoản không có thẩm quyền truy cập"


class TestRegisterAPI:
    @patch("src.modules.auth_profiles.views.register_user_service")
    def test_register_success(self, mock_service, configured_client):
        mock_service.return_value = ({"id": 1}, "SUCCESS")
        payload = {
            "email": "test@example.com", "password": "Password123@",
            "firstName": "John", "lastName": "Doe", "dayOfBirth": "1990-01-01",
            "gender": "MALE", "phone": "0123456789"
        }
        response = configured_client.post("/auth/register", json=payload)
        assert response.status_code == 201

    def test_register_missing_fields(self, configured_client):
        payload = {"email": "test@example.com"}
        response = configured_client.post("/auth/register", json=payload)
        assert response.status_code == 400

    def test_register_invalid_regex(self, configured_client):
        payload = {
            "email": "invalid", "password": "123",
            "firstName": "John", "lastName": "Doe", "dayOfBirth": "1990-01-01",
            "gender": "MALE", "phone": "0123456789"
        }
        response = configured_client.post("/auth/register", json=payload)
        assert response.status_code == 400

    def test_register_xss_violation(self, configured_client):
        payload = {
            "email": "test@example.com", "password": "Password123@",
            "firstName": "<script>alert(1)</script>", "lastName": "Doe",
            "dayOfBirth": "1990-01-01", "gender": "MALE", "phone": "0123456789"
        }
        response = configured_client.post("/auth/register", json=payload)
        assert response.status_code == 400

    @patch("src.modules.auth_profiles.views.register_user_service")
    def test_register_duplicate_email(self, mock_service, configured_client):
        mock_service.return_value = (None, "ERROR_BAD_REQUEST")
        payload = {
            "email": "test@example.com", "password": "Password123@",
            "firstName": "John", "lastName": "Doe", "dayOfBirth": "1990-01-01",
            "gender": "MALE", "phone": "0123456789"
        }
        response = configured_client.post("/auth/register", json=payload)
        assert response.status_code == 400


class TestEmailValidatorAPI:
    @patch("src.modules.auth_profiles.views.check_email_exists_service")
    def test_email_validator_valid(self, mock_service, configured_client):
        mock_service.return_value = True
        payload = {"email": "new@example.com"}
        response = configured_client.post("/auth/email-validator", json=payload)
        assert response.status_code == 200
        assert response.json["is_valid"] is True

    def test_email_validator_invalid(self, configured_client):
        payload = {"email": "invalid_email"}
        response = configured_client.post("/auth/email-validator", json=payload)
        assert response.status_code == 400
        assert response.json["is_valid"] is False

    @patch("src.modules.auth_profiles.views.check_email_exists_service")
    def test_email_validator_exists(self, mock_service, configured_client):
        mock_service.return_value = False
        payload = {"email": "exist@example.com"}
        response = configured_client.post("/auth/email-validator", json=payload)
        assert response.status_code == 400
        assert response.json["is_valid"] is False

    def test_email_validator_missing(self, configured_client):
        payload = {}
        response = configured_client.post("/auth/email-validator", json=payload)
        assert response.status_code == 400


class TestRetrieveCurrentUserAPI:
    @patch("src.modules.auth_profiles.views.get_user_data")
    def test_get_user_success(self, mock_service, configured_client, valid_header):
        mock_service.return_value = {"id": 1, "username": "testuser"}
        response = configured_client.get("/auth/current-user", headers=valid_header)
        assert response.status_code == 200
        assert response.json["user"]["username"] == "testuser"

    def test_get_user_no_token(self, configured_client):
        response = configured_client.get("/auth/current-user")
        assert response.status_code != 200

    @patch("src.modules.auth_profiles.views.update_patient_profile_service")
    def test_patch_user_success(self, mock_service, configured_client, valid_header):
        mock_service.return_value = ({"id": 1, "firstName": "Updated"}, "SUCCESS")
        payload = {"firstName": "Updated"}
        response = configured_client.patch("/auth/current-user", json=payload, headers=valid_header)
        assert response.status_code == 200

    def test_patch_user_xss_violation(self, configured_client, valid_header):
        payload = {"firstName": "<script>"}
        response = configured_client.patch("/auth/current-user", json=payload, headers=valid_header)
        assert response.status_code == 400

    @patch("src.modules.auth_profiles.views.update_patient_profile_service")
    def test_patch_user_not_patient(self, mock_service, configured_client, valid_header):
        mock_service.return_value = (None, "FORBIDDEN")
        payload = {"firstName": "Updated"}
        response = configured_client.patch("/auth/current-user", json=payload, headers=valid_header)
        assert response.status_code == 403

    @patch("src.modules.auth_profiles.views.get_user_data")
    def test_get_user_data_error(self, mock_service, configured_client, valid_header):
        mock_service.return_value = None
        response = configured_client.get("/auth/current-user", headers=valid_header)
        assert response.status_code == 500
        assert response.json["message"] == "Có vấn đề trong lấy thông tin người dùng"

    @patch("src.modules.auth_profiles.views.update_patient_profile_service")
    def test_patch_bad_request_error(self, mock_service, configured_client, valid_header):
        mock_service.return_value = (None, "ERROR_BAD_REQUEST")
        payload = {"dayOfBirth": "invalid-date"}
        response = configured_client.patch("/auth/current-user", json=payload, headers=valid_header)
        assert response.status_code == 400
        assert response.json["message"] == "Sai định dạng ngày sinh hoặc không có hồ sơ"
