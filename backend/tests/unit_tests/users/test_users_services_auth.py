from unittest.mock import patch

import jwt
import pytest
from werkzeug.security import generate_password_hash

from src.modules.users.models import PatientProfile, User, UserRole
from src.modules.users.services import create_token
from tests.unit_tests.test_base import test_app, test_session


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def valid_register_payload():
    return {
        "username": "juniorthanh09",
        "password": generate_password_hash("Admin123@"),
        "email": "juniorthanh09@example.com",
        "first_name": "Trung Thành",
        "last_name": "Văn",
        "gender": "MALE",
        "phone": "0123456789",
        "birthday": "2005-11-13",
    }


@pytest.fixture
def active_user(test_session):
    user = User(
        username="activeuser",
        password=generate_password_hash("password123"),
        email="active@example.com",
        first_name="Active",
        last_name="User",
        role=UserRole.PATIENT,
        is_active=True,
    )
    test_session.add(user)
    test_session.commit()

    profile = PatientProfile(user_id=user.id, phone="0987654321")
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def inactive_user(test_session):
    user = User(
        username="inactiveuser",
        password=generate_password_hash("password123"),
        email="inactive@example.com",
        first_name="Inactive",
        last_name="User",
        role=UserRole.PATIENT,
        is_active=False,
    )
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def auth_headers(test_app, active_user):
    with test_app.app_context():
        token = create_token(active_user)
        return {"Authorization": f"Bearer {token}"}


def test_register_success(client, test_session, valid_register_payload):
    response = client.post("/api/v1/auth/register", json=valid_register_payload)
    assert response.status_code == 201
    assert response.json["message"] == "Đăng ký thành công"

    saved_user = test_session.query(User).filter_by(username="juniorthanh09").first()
    assert saved_user is not None


def test_register_dup_username(client, active_user, valid_register_payload):
    payload = {**valid_register_payload, "username": active_user.username}
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json["message"] == "Username đã tồn tại"


def test_register_dup_email(client, active_user, valid_register_payload):
    payload = {**valid_register_payload, "email": active_user.email}
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert response.json["message"] == "Email đã tồn tại"


def test_register_invalid_birthday(client, valid_register_payload):
    payload = {**valid_register_payload, "birthday": "01-01-2000"}
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert "Sai định dạng ngày sinh" in response.json["message"]


@patch("src.modules.users.services.cloudinary.uploader.upload")
def test_register_with_avatar(mock_upload, client, valid_register_payload):
    mock_upload.return_value = {"secure_url": "https://cloudinary.com/image.png"}
    payload = {**valid_register_payload, "avatar": "base64_image_data"}
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 201
    assert (
        response.json["user"]["profile"]["avatar"] == "https://cloudinary.com/image.png"
    )


@patch("src.modules.users.services.db.session.commit")
def test_register_db_exception(mock_commit, client, valid_register_payload):
    mock_commit.side_effect = Exception("DB Connection Lost")
    response = client.post("/api/v1/auth/register", json=valid_register_payload)
    assert response.status_code == 500
    assert response.json["message"] == "Có lỗi xảy ra trong quá trình đăng ký!"


def test_login_success(client, active_user):
    payload = {"email": "active@example.com", "password": "password123"}
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    assert "token" in response.json


def test_login_wrong_pass(client, active_user):
    payload = {"email": "active@example.com", "password": "wrongpassword"}
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401


def test_login_no_user(client):
    payload = {"email": "nobody", "password": "password123"}
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401


def test_login_inactive(client, inactive_user):
    payload = {"email": "inactive@example.com", "password": "password123"}
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 403


@patch("src.modules.users.services.verify_google_token")
def test_google_login_success(mock_verify, client, test_session):
    mock_verify.return_value = {"email": "newgoogle@example.com", "name": "Google User"}
    payload = {"token": "valid_google_token"}
    response = client.post("/api/v1/auth/google-login", json=payload)
    assert response.status_code == 200
    assert "token" in response.json


@patch("src.modules.users.services.verify_google_token")
def test_google_login_invalid(mock_verify, client):
    mock_verify.return_value = None
    payload = {"token": "invalid_google_token"}
    response = client.post("/api/v1/auth/google-login", json=payload)
    assert response.status_code == 401


@patch("src.modules.users.services.verify_google_token")
def test_google_login_existing_user(mock_verify, client, active_user):
    mock_verify.return_value = {"email": active_user.email, "name": "Active User"}
    payload = {"token": "valid_google_token"}
    response = client.post("/api/v1/auth/google-login", json=payload)
    assert response.status_code == 200
    assert response.json["message"] == "Đăng nhập Google thành công"
    assert "token" in response.json


def test_get_current_user_success(client, auth_headers):
    response = client.get("/api/v1/auth/current-user", headers=auth_headers)
    assert response.status_code == 200
    assert response.json["data"]["username"] == "activeuser"


@patch("src.modules.users.services.jwt.decode")
def test_token_expired(mock_jwt_decode, client, auth_headers):
    mock_jwt_decode.side_effect = jwt.ExpiredSignatureError()
    response = client.get("/api/v1/auth/current-user", headers=auth_headers)
    assert response.status_code == 401
    assert response.json["message"] == "Token đã hết hạn"


@patch("src.modules.users.services.jwt.decode")
def test_token_invalid(mock_jwt_decode, client, auth_headers):
    mock_jwt_decode.side_effect = jwt.InvalidTokenError()
    response = client.get("/api/v1/auth/current-user", headers=auth_headers)
    assert response.status_code == 401
    assert response.json["message"] == "Token không hợp lệ"


def test_patch_profile_success(client, auth_headers):
    payload = {"first_name": "Updated", "address": "123 New Street"}
    response = client.patch(
        "/api/v1/auth/current-user", json=payload, headers=auth_headers
    )
    assert response.status_code == 200
    assert response.json["data"]["first_name"] == "Updated"
    assert response.json["data"]["profile"]["address"] == "123 New Street"


def test_patch_profile_invalid_date(client, auth_headers):
    payload = {"birthday": "01-01-2000"}
    response = client.patch(
        "/api/v1/auth/current-user", json=payload, headers=auth_headers
    )
    assert response.status_code == 400
    assert "Vui lòng định dạng theo YYYY-mm-dd" in response.json["message"]


def test_patch_profile_not_patient(client, test_app, test_session):
    doc_user = User(
        username="doctor",
        email="doc@gmail.com",
        password="123",
        first_name="Test",
        last_name="Doctor",
        role=UserRole.DOCTOR,
        is_active=True,
    )
    test_session.add(doc_user)
    test_session.commit()

    with test_app.app_context():
        token = create_token(doc_user)

    response = client.patch(
        "/api/v1/auth/current-user",
        json={"first_name": "Test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403
    assert "Chỉ có bệnh nhân" in response.json["message"]


def test_patch_profile_no_profile_exists(client, test_app, test_session):
    new_patient = User(
        username="nopatient",
        email="no@gmail.com",
        password="123",
        first_name="Test",
        last_name="Patient",
        role=UserRole.PATIENT,
        is_active=True,
    )
    test_session.add(new_patient)
    test_session.commit()

    with test_app.app_context():
        token = create_token(new_patient)

    response = client.patch(
        "/api/v1/auth/current-user",
        json={"first_name": "Test"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
    assert "Hồ sơ chưa tồn tại" in response.json["message"]
