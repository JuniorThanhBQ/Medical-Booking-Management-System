import pytest

from tests.test_base import test_app


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_index_status_code_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.data.decode("utf-8") == "OK"


def test_index_not_found(client):
    response = client.get("/non-existent-page")

    assert response.status_code == 404


def test_health_status_200(client):
    response = client.get("/health")
    json_data = response.get_json()

    assert response.status_code == 200
    assert json_data["status"] == "good"
    assert json_data["message"] == "Backend đã chạy"
