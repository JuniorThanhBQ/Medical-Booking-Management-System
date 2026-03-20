from unittest.mock import patch

import pytest

from src.modules.users.models import PatientProfile, User
from tests.unit_tests.test_base import test_app, test_session


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_patient_lifecycle(client, test_session):
    register_payload = {
        "username": "juniorthanh09",
        "password": "Admin123@",
        "email": "2351050164thanh@ou.edu.vn",
        "first_name": "Trung Thành",
        "last_name": "Văn",
        "gender": "MALE",
        "phone": "0987654321",
        "birthday": "2005-11-13",
    }

    res_register = client.post("/api/v1/auth/register", json=register_payload)
    assert res_register.status_code == 201
    assert res_register.json["message"] == "Đăng ký thành công"

    login_payload = {"email": "2351050164thanh@ou.edu.vn", "password": "Admin123@"}

    res_login = client.post("/api/v1/auth/login", json=login_payload)
    assert res_login.status_code == 200
    assert "token" in res_login.json

    token = res_login.json["token"]
    auth_headers = {"Authorization": f"Bearer {token}"}

    patch_payload = {
        "first_name": "Thành",
        "address": "97 Võ Văn Tần",
        "medical_history": "Không có bệnh lý nền, sức khỏe tốt",
    }
    res_patch = client.patch(
        "/api/v1/auth/current-user", json=patch_payload, headers=auth_headers
    )
    assert res_patch.status_code == 200
    assert res_patch.json["message"] == "Cập nhật hồ sơ thành công"

    res_get = client.get("/api/v1/auth/current-user", headers=auth_headers)
    assert res_get.status_code == 200

    data = res_get.json["data"]
    assert data["username"] == "juniorthanh09"
    assert data["first_name"] == "Thành"
    assert data["email"] == "2351050164thanh@ou.edu.vn"

    assert data["profile"]["address"] == "97 Võ Văn Tần"
    assert data["profile"]["medical_history"] == "Không có bệnh lý nền, sức khỏe tốt"
    assert data["profile"]["phone"] == "0987654321"

    user_in_db = test_session.query(User).filter_by(username="juniorthanh09").first()
    assert user_in_db is not None
    assert user_in_db.first_name == "Thành"
    assert user_in_db.is_active is True

    profile_in_db = (
        test_session.query(PatientProfile).filter_by(user_id=user_in_db.id).first()
    )
    assert profile_in_db is not None
    assert profile_in_db.address == "97 Võ Văn Tần"
    assert profile_in_db.medical_history == "Không có bệnh lý nền, sức khỏe tốt"


def test_patient_registration_and_validation_flow(client, test_session):
    bad_payload = {"username": "juniorthanh09"}
    res_bad = client.post("/api/v1/auth/register", json=bad_payload)
    assert res_bad.status_code == 400
    assert "Vui lòng điền đầy đủ thông tin" in res_bad.json["message"]

    valid_payload = {
        "username": "juniorthanh09",
        "password": "Admin123@",
        "email": "2351050164thanh@ou.edu.vn",
        "first_name": "Trung Thành",
        "last_name": "Văn",
        "gender": "MALE",
        "phone": "0987654321",
        "birthday": "1995-05-20",
    }
    res_success = client.post("/api/v1/auth/register", json=valid_payload)
    assert res_success.status_code == 201

    res_dup = client.post("/api/v1/auth/register", json=valid_payload)
    assert res_dup.status_code == 400
    assert "tồn tại" in res_dup.json["message"]

    res_login_fail = client.post(
        "/api/v1/auth/login",
        json={"email": "juniorthanh09@ou.edu.vn", "password": "wrong"},
    )
    assert res_login_fail.status_code == 401

    res_login_ok = client.post(
        "/api/v1/auth/login",
        json={"email": "2351050164thanh@ou.edu.vn", "password": "Admin123@"},
    )
    assert "token" in res_login_ok.json
    token = res_login_ok.json["token"]
    headers = {"Authorization": f"Bearer {token}"}

    res_patch_fail = client.patch(
        "/api/v1/auth/current-user", json={"birthday": "13-11-2005"}, headers=headers
    )
    assert res_patch_fail.status_code == 400
    assert "định dạng" in res_patch_fail.json["message"]

    res_patch_ok = client.patch(
        "/api/v1/auth/current-user", json={"address": "123 Tích Hợp"}, headers=headers
    )
    assert res_patch_ok.status_code == 200
    assert res_patch_ok.json["data"]["profile"]["address"] == "123 Tích Hợp"


@patch("src.modules.users.services.verify_google_token")
def test_google_sso_and_profile_flow(mock_verify, client, test_session):
    mock_verify.return_value = {
        "email": "google_int@example.com",
        "name": "Google User",
    }

    res_google = client.post(
        "/api/v1/auth/google-login", json={"token": "fake-google-token"}
    )
    assert res_google.status_code == 200
    token = res_google.json["token"]
    headers = {"Authorization": f"Bearer {token}"}

    res_get = client.get("/api/v1/auth/current-user", headers=headers)
    assert res_get.status_code == 200
    assert res_get.json["data"]["email"] == "google_int@example.com"
    assert res_get.json["data"]["profile"] is None

    res_patch = client.patch(
        "/api/v1/auth/current-user", json={"phone": "123456789"}, headers=headers
    )
    assert res_patch.status_code == 400
    assert "Hồ sơ chưa tồn tại" in res_patch.json["message"]
