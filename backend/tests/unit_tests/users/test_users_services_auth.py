from unittest.mock import patch

import pytest
from src.modules.users.models import User, UserRole
from tests.unit_tests.test_base import test_app, test_session
from werkzeug.security import generate_password_hash


@pytest.fixture
def client(test_app):
    return test_app.test_client()


@pytest.fixture
def valid_register_payload():
    return {
        "username": "newuser",
        "password": "securepassword",
        "email": "newuser@example.com",
        "first_name": "New",
        "last_name": "User",
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


def test_register_happy_path(client, test_session, valid_register_payload):
    response = client.post("/api/v1/auth/register", json=valid_register_payload)

    assert response.status_code == 201
    assert response.json["message"] == "Đăng ký thành công"
    assert response.json["user"]["username"] == "newuser"

    saved_user = test_session.query(User).filter_by(username="newuser").first()
    assert saved_user is not None
    assert saved_user.email == "newuser@example.com"


def test_register_missing_fields_invalid_input(client):
    payload = {"username": "testuser"}
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 400
    assert (
        "Vui lòng điền đầy đủ thông tin bắt buộc" in response.json["message"]
        or "email" in response.json["message"]
    )


def test_register_duplicate_username_edge_case(
    client, active_user, valid_register_payload
):
    payload = {**valid_register_payload, "username": active_user.username}
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json["message"] == "Username đã tồn tại"


def test_register_duplicate_email_edge_case(
    client, active_user, valid_register_payload
):
    payload = {**valid_register_payload, "email": active_user.email}
    response = client.post("/api/v1/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json["message"] == "Email đã tồn tại"


def test_login_happy_path(client, active_user):
    payload = {"username": "activeuser", "password": "password123"}
    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == 200
    assert response.json["message"] == "Đăng nhập thành công"
    assert "token" in response.json


def test_login_wrong_password_invalid_input(client, active_user):
    payload = {"username": "activeuser", "password": "wrongpassword"}
    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json["message"] == "Tài khoản hoặc mật khẩu có thể không đúng"


def test_login_nonexistent_user_invalid_input(client):
    payload = {"username": "nobody", "password": "password123"}
    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == 401
    assert response.json["message"] == "Tài khoản hoặc mật khẩu có thể không đúng"


def test_login_inactive_user_edge_case(client, inactive_user):
    payload = {"username": "inactiveuser", "password": "password123"}
    response = client.post("/api/v1/auth/login", json=payload)

    assert response.status_code == 403
    assert response.json["message"] == "Tài khoản đã bị khóa"


@patch("src.modules.users.services.verify_google_token")
def test_google_login_happy_path_new_user(mock_verify, client, test_session):
    mock_verify.return_value = {"email": "newgoogle@example.com", "name": "Google User"}
    payload = {"token": "valid_google_token"}
    response = client.post("/api/v1/auth/google-login", json=payload)

    assert response.status_code == 200
    assert response.json["message"] == "Đăng nhập Google thành công"
    assert "token" in response.json

    saved_user = (
        test_session.query(User).filter_by(email="newgoogle@example.com").first()
    )
    assert saved_user is not None
    assert saved_user.first_name == "Google"
    assert saved_user.last_name == "User"


@patch("src.modules.users.services.verify_google_token")
def test_google_login_invalid_token_edge_case(mock_verify, client):
    mock_verify.return_value = None
    payload = {"token": "invalid_google_token"}
    response = client.post("/api/v1/auth/google-login", json=payload)

    assert response.status_code == 401
    assert response.json["message"] == "Google token không hợp lệ"
