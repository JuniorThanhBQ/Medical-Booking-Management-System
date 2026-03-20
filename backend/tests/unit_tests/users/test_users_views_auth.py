import pytest

from tests.unit_tests.test_base import test_app


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_register_missing_fields(client):
    payload = {"username": "juniorthanh09"}
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400
    assert "Vui lòng điền đầy đủ thông tin bắt buộc" in response.json["message"]


def test_get_current_user_no_token(client):
    response = client.get("/api/v1/auth/current-user")
    assert response.status_code == 401


def test_token_missing_bearer(client):
    response = client.get(
        "/api/v1/auth/current-user", headers={"Authorization": "Token 123"}
    )
    assert response.status_code == 401
    assert response.json["message"] == "Có vấn đề trong xác thực token"
