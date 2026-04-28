from tests.test_base import test_app, test_client

def test_index_status_code_200(test_client):
    res = test_client.get("/")

    assert res.status_code == 200
    assert res.data.decode("utf-8") == "OK"


def test_index_not_found(test_client):
    res = test_client.get("/non-existent-page")

    assert res.status_code == 404


def test_health_status_200(test_client):
    res = test_client.get("/health")
    data = res.get_json()

    assert res.status_code == 200
    assert data["status"] == "good"
    assert data["message"] == "Backend đã chạy"
