from unittest.mock import patch

import pytest
from werkzeug.security import generate_password_hash

from src.modules.users.models import PatientProfile, User, UserRole
from src.modules.users.repositories import add_profile, add_user, commit
from src.utils.users.jwt_utils import create_token
from tests.test_base import test_app, test_session


@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

def seed_db(app):
    with app.app_context():
        user = User(
            username="view_user", password=generate_password_hash("StrongPassword@123"),
            email="view@test.com", first_name="View", last_name="User", role=UserRole.PATIENT
        )
        add_user(user)
        add_profile(PatientProfile(user_id=user.id, phone="0111222333"))
        commit()
        return user, create_token(user)

def test_login_api(test_client, test_app, test_session):
    seed_db(test_app)

    res = test_client.post('/api/v1/auth/login', json={"email": "view@test.com"})
    assert res.status_code == 400

    res = test_client.post('/api/v1/auth/login', json={"email": "view@test.com", "password": "123", "role": "PATIENT"})
    assert res.status_code == 400

    res = test_client.post('/api/v1/auth/login', json={"email": "view@test.com",
                                                       "password": "StrongPassword@123",
                                                       "role": "PATIENT"})
    assert res.status_code == 201
    data = res.get_json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert "refresh_token" in res.headers.get("Set-Cookie", "")

@patch('src.modules.users.views.verify_email_existence', return_value=True)
@patch('src.modules.users.services.cloudinary_upload_process', return_value="url")
def test_register_api(mock_cloudinary, mock_verify_email, test_client, test_app, test_session):
    res = test_client.post('/api/v1/auth/register', json={"email": "new@test.com"})
    assert res.status_code == 400

    payload = {
        "email": "new_view@test.com", "password": "StrongPassword@123",
        "firstName": "A", "lastName": "B", "dayOfBirth": "2000-01-01",
        "gender": "male", "phone": "0123"
    }

    xss_payload = payload.copy()
    xss_payload["firstName"] = "<script>alert(1)</script>"
    res = test_client.post('/api/v1/auth/register', json=xss_payload)
    assert res.status_code == 400

    mock_verify_email.return_value = False
    res = test_client.post('/api/v1/auth/register', json=payload)
    assert res.status_code == 400

    mock_verify_email.return_value = True
    res = test_client.post('/api/v1/auth/register', json=payload)
    assert res.status_code == 201


def test_retrieve_current_user_api(test_client, test_app, test_session):
    user, token = seed_db(test_app)
    headers = {"Authorization": f"Bearer {token}"}

    res = test_client.get('/api/v1/auth/current-user', headers=headers)
    assert res.status_code == 200
    assert res.get_json()["user"]["email"] == "view@test.com"

    res = test_client.patch('/api/v1/auth/current-user', headers=headers, json={"firstName": "<h1>Hacked</h1>"})
    assert res.status_code == 400

    res = test_client.patch('/api/v1/auth/current-user', headers=headers, json={"firstName": "SafeName"})
    assert res.status_code == 200