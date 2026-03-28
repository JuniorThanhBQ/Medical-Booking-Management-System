from datetime import date, datetime
from unittest.mock import patch

import pytest
from flask_restx import Api

from src.modules.appointments.models import Appointment, StatusRole
from src.modules.appointments.views import appointments_namespace
from src.modules.auth_profiles.models import (DoctorProfile, GenderRole,
                                              PatientProfile, Specialty, User,
                                              UserRole)
from src.utils.utils import create_token
from tests.test_base import test_app, test_session


@pytest.fixture
def integration_client(test_app):
    if hasattr(appointments_namespace, 'apis'):
        appointments_namespace.apis.clear()

    api = Api(test_app)
    api.add_namespace(appointments_namespace, path="/appointments")
    return test_app.test_client()


@pytest.fixture
def integration_patient(test_session):
    user = User(
        username="patient_user",
        password="hashed_password",
        email="patient@clinic.com",
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
        birthday=date(1990, 1, 1),
        address="123 Street"
    )
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def integration_doctor(test_session):
    user = User(
        username="doctor_user",
        password="hashed_password",
        email="doctor@clinic.com",
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
        title="Dr.",
        bio="Expert",
        specialty_id=specialty.id
    )
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def integration_admin(test_session):
    user = User(
        username="admin_user",
        password="hashed_password",
        email="admin@clinic.com",
        first_name="Super",
        last_name="Admin",
        is_active=True
    )
    user.role = UserRole.ADMIN
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def integration_reception(test_session):
    user = User(
        username="reception_user",
        password="hashed_password",
        email="reception@clinic.com",
        first_name="Anna",
        last_name="Taylor",
        is_active=True
    )
    user.role = UserRole.RECEPTIONIST
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def integration_appointment(test_session, integration_patient, integration_doctor):
    appointment = Appointment(
        name="General Checkup",
        note="Routine check",
        status=StatusRole.PENDING,
        appointment_date=datetime(2026, 1, 1, 10, 0),
        doctor_profile_id=integration_doctor.profile.id,
        patient_profile_id=integration_patient.profile.id
    )
    test_session.add(appointment)
    test_session.commit()
    return appointment


@pytest.fixture
def patient_token_header(integration_patient, test_app):
    with test_app.app_context():
        token = create_token(integration_patient)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def doctor_token_header(integration_doctor, test_app):
    with test_app.app_context():
        token = create_token(integration_doctor)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_token_header(integration_admin, test_app):
    with test_app.app_context():
        token = create_token(integration_admin)
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def reception_token_header(integration_reception, test_app):
    with test_app.app_context():
        token = create_token(integration_reception)
    return {"Authorization": f"Bearer {token}"}


class TestIntegrationPatientBookingFlow:
    @patch("src.modules.appointments.services.validate_available_slot")
    @patch("src.modules.appointments.services.validate_appointment_date")
    @patch("src.modules.appointments.services.get_doctor_by_id")
    def test_patient_booking_success(self, mock_get_doctor, mock_val_date, mock_val_slot, integration_client,
                                     patient_token_header, integration_doctor, test_session):
        mock_get_doctor.return_value = integration_doctor
        mock_val_date.return_value = (None, None)
        mock_val_slot.return_value = (None, None)

        payload = {
            "doctorId": integration_doctor.id,
            "appointmentDate": "2030-01-01T10:00:00",
            "note": "Patient needs checkup"
        }
        response = integration_client.post("/appointments", json=payload, headers=patient_token_header)
        assert response.status_code == 201

        new_appointment = test_session.query(Appointment).filter_by(note="Patient needs checkup").first()
        assert new_appointment is not None
        assert new_appointment.doctor_profile_id == integration_doctor.profile.id

    def test_patient_booking_missing(self, integration_client, patient_token_header):
        payload = {"note": "Missing doctor ID"}
        response = integration_client.post("/appointments", json=payload, headers=patient_token_header)
        assert response.status_code == 400

    def test_patient_booking_forbidden(self, integration_client, admin_token_header):
        payload = {"doctorId": 1, "appointmentDate": "2030-01-01T10:00:00", "note": "Admin booking"}
        response = integration_client.post("/appointments", json=payload, headers=admin_token_header)
        assert response.status_code == 403


class TestIntegrationReceptionistBookingFlow:
    @patch("src.modules.appointments.services.validate_available_slot")
    @patch("src.modules.appointments.services.validate_appointment_date")
    @patch("src.modules.appointments.services.get_doctor_by_id")
    def test_reception_booking_new(self, mock_get_doctor, mock_val_date, mock_val_slot, integration_client,
                                   reception_token_header, integration_doctor, test_session):
        mock_get_doctor.return_value = integration_doctor
        mock_val_date.return_value = (None, None)
        mock_val_slot.return_value = (None, None)

        payload = {
            "doctorId": integration_doctor.id,
            "appointmentDate": "2030-01-01T10:00:00",
            "note": "New patient checkup",
            "firstName": "New",
            "lastName": "Patient",
            "phone": "0999888777",
            "gender": "MALE",
            "birthday": "1995-05-05",
            "address": "456 New St"
        }
        response = integration_client.post("/appointments/receptionist-appointments", json=payload,
                                           headers=reception_token_header)
        assert response.status_code == 201

        new_user = test_session.query(User).filter_by(first_name="New", last_name="Patient").first()
        assert new_user is not None
        assert new_user.role == UserRole.PATIENT

        new_profile = test_session.query(PatientProfile).filter_by(user_id=new_user.id).first()
        assert new_profile is not None
        assert new_profile.phone == "0999888777"

        new_appointment = test_session.query(Appointment).filter_by(patient_profile_id=new_profile.id).first()
        assert new_appointment is not None

    @patch("src.modules.appointments.services.validate_available_slot")
    @patch("src.modules.appointments.services.validate_appointment_date")
    @patch("src.modules.appointments.services.get_doctor_by_id")
    def test_reception_booking_exist(self, mock_get_doctor, mock_val_date, mock_val_slot, integration_client,
                                     reception_token_header, integration_doctor, integration_patient, test_session):
        mock_get_doctor.return_value = integration_doctor
        mock_val_date.return_value = (None, None)
        mock_val_slot.return_value = (None, None)

        initial_user_count = test_session.query(User).count()

        payload = {
            "doctorId": integration_doctor.id,
            "appointmentDate": "2030-01-02T10:00:00",
            "note": "Existing patient checkup",
            "firstName": integration_patient.first_name,
            "lastName": integration_patient.last_name,
            "phone": integration_patient.profile.phone,
            "gender": "MALE",
            "birthday": "1990-01-01",
            "address": integration_patient.profile.address
        }
        response = integration_client.post("/appointments/receptionist-appointments", json=payload,
                                           headers=reception_token_header)
        assert response.status_code == 201

        final_user_count = test_session.query(User).count()
        assert final_user_count == initial_user_count

        new_appointment = test_session.query(Appointment).filter_by(note="Existing patient checkup").first()
        assert new_appointment is not None
        assert new_appointment.patient_profile_id == integration_patient.profile.id

    def test_reception_booking_deny(self, integration_client, patient_token_header):
        payload = {"doctorId": 1, "appointmentDate": "2030-01-01T10:00:00"}
        response = integration_client.post("/appointments/receptionist-appointments", json=payload,
                                           headers=patient_token_header)
        assert response.status_code == 403


class TestIntegrationRetrieveAppointmentFlow:
    def test_get_list_by_patient(self, integration_client, patient_token_header, integration_appointment):
        response = integration_client.get("/appointments", headers=patient_token_header)
        assert response.status_code == 200
        assert len(response.json["items"]) == 1
        assert response.json["items"][0]["id"] == str(integration_appointment.id)

    def test_get_list_by_admin(self, integration_client, admin_token_header, integration_appointment):
        response = integration_client.get("/appointments", headers=admin_token_header)
        assert response.status_code == 200
        assert len(response.json["items"]) == 1

    def test_get_detail_success(self, integration_client, doctor_token_header, integration_appointment):
        response = integration_client.get(f"/appointments/{integration_appointment.id}", headers=doctor_token_header)
        assert response.status_code == 200
        assert "medicalRecordId" in response.json

    def test_get_detail_forbidden(self, integration_client, integration_appointment, test_session, test_app):
        other_patient = User(
            username="other",
            password="hashed",
            email="other@clinic.com",
            first_name="Other",
            last_name="Patient",
            is_active=True
        )
        other_patient.role = UserRole.PATIENT
        test_session.add(other_patient)
        test_session.flush()

        other_profile = PatientProfile(
            user_id=other_patient.id,
            phone="111222333",
            gender=GenderRole.MALE,
            birthday=date(1990, 1, 1),
            address="ABC"
        )
        test_session.add(other_profile)
        test_session.commit()

        with test_app.app_context():
            other_token = create_token(other_patient)
        other_header = {"Authorization": f"Bearer {other_token}"}

        response = integration_client.get(f"/appointments/{integration_appointment.id}", headers=other_header)
        assert response.status_code == 403


class TestIntegrationUpdateDeleteFlow:
    @patch("src.modules.appointments.services.validate_available_slot")
    @patch("src.modules.appointments.services.validate_appointment_date")
    def test_patch_appointment_success(self, mock_val_date, mock_val_slot, integration_client, reception_token_header,
                                       integration_appointment, test_session):
        mock_val_date.return_value = (None, None)
        mock_val_slot.return_value = (None, None)
        payload = {"status": "CANCEL", "note": "Patient requested cancel"}
        response = integration_client.patch(f"/appointments/{integration_appointment.id}", json=payload,
                                            headers=reception_token_header)
        assert response.status_code == 204

        updated_appointment = test_session.get(Appointment, integration_appointment.id)
        assert updated_appointment.status == StatusRole.CANCEL
        assert updated_appointment.note == "Patient requested cancel"

    def test_delete_appointment_success(self, integration_client, admin_token_header, integration_appointment,
                                        test_session):
        integration_appointment.status = StatusRole.CANCEL
        test_session.commit()

        response = integration_client.delete(f"/appointments/{integration_appointment.id}", headers=admin_token_header)
        assert response.status_code == 204

        deleted_appointment = test_session.get(Appointment, integration_appointment.id)
        assert deleted_appointment is None

    def test_delete_invalid_status(self, integration_client, admin_token_header, integration_appointment):
        integration_appointment.status = StatusRole.APPROVED
        response = integration_client.delete(f"/appointments/{integration_appointment.id}", headers=admin_token_header)
        assert response.status_code == 400


class TestIntegrationPatientProfileFlow:
    def test_doctor_get_profile_success(self, integration_client, doctor_token_header, integration_appointment,
                                        integration_patient):
        response = integration_client.get(f"/appointments/{integration_appointment.id}/patient-profile",
                                          headers=doctor_token_header)
        assert response.status_code == 200
        assert response.json["firstName"] == integration_patient.first_name
        assert response.json["phone"] == integration_patient.profile.phone

    def test_patient_get_profile_deny(self, integration_client, patient_token_header, integration_appointment):
        response = integration_client.get(f"/appointments/{integration_appointment.id}/patient-profile",
                                          headers=patient_token_header)
        assert response.status_code == 403
