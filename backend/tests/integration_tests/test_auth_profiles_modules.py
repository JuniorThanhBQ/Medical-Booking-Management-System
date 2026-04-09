from unittest.mock import patch

import pytest
from flask_restx import Api
from werkzeug.security import generate_password_hash

from src.extensions import limiter
from src.modules.doctors.models import DoctorProfile, Specialty
from src.modules.users.models import GenderRole, PatientProfile, User, UserRole
from src.modules.users.views import auth_namespace
from src.utils.utils import create_token
from tests.test_base import test_app, test_session


@pytest.fixture
def integration_client(test_app):
    limiter.init_app(test_app)
    api = Api(test_app)
    api.add_namespace(auth_namespace, path="/auth")
    return test_app.test_client()


@pytest.fixture
def integration_patient_user(test_session):
    user = User(
        username="patientuser",
        password=generate_password_hash("Password123@"),
        email="patient@example.com",
        first_name="John",
        last_name="Doe",
        is_active=True
    )
    user.role = UserRole.PATIENT
    test_session.add(user)
    test_session.flush()

    profile = PatientProfile(
        user_id=user.id,
        phone="0123456789",
        gender=GenderRole.MALE,
        medical_history="Healthy"
    )
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def integration_doctor_user(test_session):
    user = User(
        username="doctoruser",
        password=generate_password_hash("Password123@"),
        email="doctor@example.com",
        first_name="Jane",
        last_name="Smith",
        is_active=True
    )
    user.role = UserRole.DOCTOR
    test_session.add(user)
    test_session.flush()

    specialty = Specialty(name="Cardiology", level="1")
    test_session.add(specialty)
    test_session.flush()

    profile = DoctorProfile(
        user_id=user.id,
        phone="0987654321",
        gender=GenderRole.FEMALE,
        title="Doctor",
        bio="Expert",
        specialty_id=specialty.id
    )
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def patient_authorization_header(integration_patient_user, test_app):
    with test_app.app_context():
        token = create_token(integration_patient_user)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def doctor_authorization_header(integration_doctor_user, test_app):
    with test_app.app_context():
        token = create_token(integration_doctor_user)
    return {"Authorization": f"Bearer {token}"}


class TestIntegrationRegisterFlow:
    @patch("src.modules.auth_profiles.services.cloudinary_upload_process")
    def test_register_successful_flow(self, mock_upload, integration_client, test_session):
        mock_upload.return_value = "https://fake.url/avatar.png"
        payload = {
            "email": "newuser@example.com",
            "password": "Password123@",
            "firstName": "New",
            "lastName": "User",
            "dayOfBirth": "1990-01-01",
            "gender": "MALE",
            "phone": "0999888777",
            "address": "123 Street",
            "medicalHistory": "None"
        }
        response = integration_client.post("/auth/register", json=payload)
        assert response.status_code == 201

        saved_user = test_session.query(User).filter_by(email="newuser@example.com").first()
        assert saved_user is not None
        assert saved_user.first_name == "New"

        saved_profile = test_session.query(PatientProfile).filter_by(user_id=saved_user.id).first()
        assert saved_profile is not None
        assert saved_profile.phone == "0999888777"

    def test_register_duplicate_email(self, integration_client, integration_patient_user, test_session):
        payload = {
            "email": "patient@example.com",
            "password": "Password123@",
            "firstName": "Clone",
            "lastName": "User",
            "dayOfBirth": "1990-01-01",
            "gender": "MALE",
            "phone": "0999888777"
        }
        response = integration_client.post("/auth/register", json=payload)
        assert response.status_code == 400

        duplicate_count = test_session.query(User).filter_by(email="patient@example.com").count()
        assert duplicate_count == 1

    def test_register_database_rollback(self, integration_client, test_session):
        payload = {
            "email": "rollback@example.com",
            "password": "Password123@",
            "firstName": "Rollback",
            "lastName": "User",
            "dayOfBirth": "invalid-date",
            "gender": "MALE",
            "phone": "0999888777"
        }
        response = integration_client.post("/auth/register", json=payload)
        assert response.status_code == 400

        aborted_user = test_session.query(User).filter_by(email="rollback@example.com").first()
        assert aborted_user is None


class TestIntegrationLoginFlow:
    def test_login_successful_flow(self, integration_client, integration_patient_user):
        payload = {
            "email": "patient@example.com",
            "password": "Password123@",
            "role": "PATIENT"
        }
        response = integration_client.post("/auth/login", json=payload)
        assert response.status_code == 200
        assert "access_token" in response.json
        assert response.json["user"]["email"] == "patient@example.com"

    def test_login_invalid_credential(self, integration_client, integration_patient_user):
        payload = {
            "email": "patient@example.com",
            "password": "WrongPassword123@",
            "role": "PATIENT"
        }
        response = integration_client.post("/auth/login", json=payload)
        assert response.status_code == 401
        assert "access_token" not in response.json

    def test_login_inactive_user_flow(self, integration_client, integration_patient_user, test_session):
        integration_patient_user.is_active = False
        test_session.commit()
        payload = {
            "email": "patient@example.com",
            "password": "Password123@",
            "role": "PATIENT"
        }
        response = integration_client.post("/auth/login", json=payload)
        assert response.status_code == 403


class TestIntegrationUpdateProfile:
    @patch("src.modules.auth_profiles.services.cloudinary_upload_process")
    def test_update_patient_success(self, mock_upload, integration_client, patient_authorization_header, test_session):
        mock_upload.return_value = "https://fake.url/new_avatar.png"
        payload = {
            "phone": "0111222333",
            "address": "456 New Avenue"
        }
        response = integration_client.patch("/auth/current-user", json=payload, headers=patient_authorization_header)
        assert response.status_code == 200

        updated_profile = test_session.query(PatientProfile).first()
        assert updated_profile.phone == "0111222333"
        assert updated_profile.address == "456 New Avenue"

    def test_update_doctor_forbidden(self, integration_client, doctor_authorization_header):
        payload = {
            "phone": "0111222333"
        }
        response = integration_client.patch("/auth/current-user", json=payload, headers=doctor_authorization_header)
        assert response.status_code == 403


class TestIntegrationEmailValidation:
    def test_email_exists_check_flow(self, integration_client, integration_patient_user):
        payload = {"email": "patient@example.com"}
        response = integration_client.post("/auth/email-validator", json=payload)
        assert response.status_code == 400
        assert response.json["is_valid"] is False

    def test_email_available_check_flow(self, integration_client):
        payload = {"email": "fresh_email@example.com"}
        response = integration_client.post("/auth/email-validator", json=payload)
        assert response.status_code == 200
        assert response.json["is_valid"] is True
