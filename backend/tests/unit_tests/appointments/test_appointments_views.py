from unittest.mock import patch

import pytest
from flask_restx import Api

from src.modules.appointments.views import (AppointmentListCreateAPI,
                                            AppointmentRetrieveUpdateDeleteAPI,
                                            PatientRetrieveAPI,
                                            ReceptionistAppointmentCreateAPI,
                                            appointments_namespace)
from src.modules.auth_profiles.models import User, UserRole
from src.utils.utils import create_token
from tests.test_base import test_app, test_session


@pytest.fixture
def configured_client(test_app):
    if hasattr(appointments_namespace, 'apis'):
        appointments_namespace.apis.clear()

    api = Api(test_app)

    if not appointments_namespace.resources:
        appointments_namespace.add_resource(AppointmentListCreateAPI, "")
        appointments_namespace.add_resource(AppointmentRetrieveUpdateDeleteAPI, "/<int:appointment_id>")
        appointments_namespace.add_resource(PatientRetrieveAPI, "/<int:appointment_id>/patient-profile")
        appointments_namespace.add_resource(ReceptionistAppointmentCreateAPI, "/receptionist-appointments")

    api.add_namespace(appointments_namespace, path="/appointments")
    return test_app.test_client()


@pytest.fixture
def mock_user(test_session):
    user = User(
        username="testuser",
        password="hashed_password",
        email="test@example.com",
        first_name="Test",
        last_name="User"
    )
    user.role = UserRole.PATIENT
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def valid_header(mock_user, test_app):
    with test_app.app_context():
        token = create_token(mock_user)
    return {"Authorization": f"Bearer {token}"}


class TestAppointmentListCreateAPI:
    @patch("src.modules.appointments.views.get_appointments_list_service")
    def test_get_appointment_list_success(self, mock_service, configured_client, valid_header):
        mock_service.return_value = ({"items": []}, "SUCCESS")
        response = configured_client.get("/appointments?page=1&limit=10", headers=valid_header)
        assert response.status_code == 200

    @patch("src.modules.appointments.views.create_patient_appointment_service")
    def test_post_appointment_create_success(self, mock_service, configured_client, valid_header):
        mock_service.return_value = ({"id": 1}, "SUCCESS")
        payload = {"doctorId": 1, "appointmentDate": "2026-01-01T10:00:00", "note": "Checkup"}
        response = configured_client.post("/appointments", json=payload, headers=valid_header)
        assert response.status_code == 201

    @patch("src.modules.appointments.views.create_patient_appointment_service")
    def test_post_appointment_missing_input(self, mock_service, configured_client, valid_header):
        mock_service.return_value = (None, "ERROR_BAD_REQUEST")
        payload = {"note": "Missing data"}
        response = configured_client.post("/appointments", json=payload, headers=valid_header)
        assert response.status_code == 400

    def test_post_appointment_xss_violation(self, configured_client, valid_header):
        payload = {"doctorId": 1, "appointmentDate": "2026-01-01", "note": "<script>alert(1)</script>"}
        response = configured_client.post("/appointments", json=payload, headers=valid_header)
        assert response.status_code == 400


class TestAppointmentRetrieveUpdateDeleteAPI:
    @patch("src.modules.appointments.views.get_appointment_detail_service")
    def test_get_appointment_detail_success(self, mock_service, configured_client, valid_header):
        mock_service.return_value = ({"id": 1}, "SUCCESS")
        response = configured_client.get("/appointments/1", headers=valid_header)
        assert response.status_code == 200

    @patch("src.modules.appointments.views.patch_appointment_service")
    def test_patch_appointment_success(self, mock_service, configured_client, valid_header):
        mock_service.return_value = ({"id": 1}, "SUCCESS")
        payload = {"status": "APPROVED", "note": "Updated"}
        response = configured_client.patch("/appointments/1", json=payload, headers=valid_header)
        assert response.status_code == 204

    def test_patch_appointment_xss_violation(self, configured_client, valid_header):
        payload = {"note": "<script>"}
        response = configured_client.patch("/appointments/1", json=payload, headers=valid_header)
        assert response.status_code == 400

    @patch("src.modules.appointments.views.delete_appointment_service")
    def test_delete_appointment_success(self, mock_service, configured_client, valid_header):
        mock_service.return_value = ({"id": 1}, "SUCCESS")
        response = configured_client.delete("/appointments/1", headers=valid_header)
        assert response.status_code == 204


class TestReceptionistAppointmentCreateAPI:
    @patch("src.modules.appointments.views.create_receptionist_appointment_service")
    def test_post_receptionist_create_success(self, mock_service, configured_client, valid_header):
        mock_service.return_value = ({"id": 2}, "SUCCESS")
        payload = {
            "doctorId": 1, "appointmentDate": "2026-01-01", "note": "Checkup",
            "firstName": "John", "lastName": "Doe", "phone": "0123456789",
            "gender": "MALE", "birthday": "1990-01-01", "address": "123 St"
        }
        response = configured_client.post("/appointments/receptionist-appointments",
                                          json=payload, headers=valid_header)
        assert response.status_code == 201

    @patch("src.modules.appointments.views.create_receptionist_appointment_service")
    def test_post_receptionist_missing_input(self, mock_service, configured_client, valid_header):
        mock_service.return_value = (None, "ERROR_BAD_REQUEST")
        payload = {"doctorId": 1}
        response = configured_client.post("/appointments/receptionist-appointments",
                                          json=payload, headers=valid_header)
        assert response.status_code == 400

    def test_post_receptionist_xss_violation(self, configured_client, valid_header):
        payload = {
            "doctorId": 1, "appointmentDate": "2026-01-01", "note": "Checkup",
            "firstName": "<script>", "lastName": "Doe", "phone": "0123456789",
            "gender": "MALE", "birthday": "1990-01-01", "address": "123 St"
        }
        response = configured_client.post("/appointments/receptionist-appointments",
                                          json=payload, headers=valid_header)
        assert response.status_code == 400


class TestPatientRetrieveAPI:
    @patch("src.modules.appointments.views.get_patient_profile_service")
    def test_get_patient_profile_success(self, mock_service, configured_client, valid_header):
        mock_service.return_value = ({"firstName": "John"}, "SUCCESS")
        response = configured_client.get("/appointments/1/patient-profile", headers=valid_header)
        assert response.status_code == 200
