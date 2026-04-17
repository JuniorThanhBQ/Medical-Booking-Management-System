import pytest
from flask import json

from src.extensions import db
from src.modules.users.models import User
from tests.test_base import test_app


@pytest.fixture
def client(test_app):
    return test_app.test_client()


def test_user_registration_duplicate_email(client, test_app):
    with test_app.app_context():
        user = User(username="existing", password="hashed", first_name="Jane", last_name="Doe", email="jane@example.com")
        db.session.add(user)
        db.session.commit()

        data = {
            "username": "newuser",
            "password": "password123",
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane@example.com",
            "role": "PATIENT"
        }
        response = client.post('/api/v1/auth/register', json=data)
        assert response.status_code == 400


def test_user_login_success(client, test_app):
    with test_app.app_context():
        from werkzeug.security import generate_password_hash
        user = User(username="testuser", password=generate_password_hash("Password@123"), first_name="John", last_name="Doe", email="john@example.com")
        db.session.add(user)
        db.session.commit()

        data = {"email": "john@example.com", "password": "Password@123", "role": "patient"}
        response = client.post('/api/v1/auth/login', json=data)
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert "access_token" in response_data
        assert "refresh_token" in response_data
        assert "refresh_token" in response.headers.get("Set-Cookie", "")
        assert response_data['user']['email'] == "john@example.com"


def test_user_login_invalid_credentials(client, test_app):
    with test_app.app_context():
        data = {"email": "nonexistent@example.com", "password": "Wrongpa@123ss", "role": "patient"}
        response = client.post('/api/v1/auth/login', json=data)
        assert response.status_code == 401


def test_retrieve_current_user_unauthenticated(client):
    response = client.get('/api/v1/auth/current-user')
    assert response.status_code == 401