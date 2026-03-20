import pytest
from tests.unit_tests.test_base import test_app, test_session


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_index_route_status_code_is_200(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.data.decode("utf-8") == "OK"


def test_index_route_not_found(client):
    response = client.get("/non-existent-page")

    assert response.status_code == 404
