from datetime import date, datetime
from unittest.mock import MagicMock, patch

import pytest

from src.modules.appointments.models import Appointment, StatusRole
from src.modules.appointments.services import (
    create_patient_appointment_service,
    create_receptionist_appointment_service, delete_appointment_service,
    get_appointment_detail_service, get_appointments_list_service,
    get_or_create_patient, get_patient_profile_service, handle_date_update,
    handle_status_update, patch_appointment_service,
    validate_appointment_booking, validate_appointment_request,
    validate_doctor)
from src.modules.auth_profiles.models import (DoctorProfile, GenderRole,
                                              PatientProfile, Specialty, User,
                                              UserRole)
from tests.test_base import test_app, test_session


@pytest.fixture
def basic_patient(test_session):
    user = User(
        username="patient_user",
        password="hashed_password",
        first_name="John",
        last_name="Doe",
        email="patient@clinic.com",
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
def basic_doctor(test_session):
    user = User(
        username="doctor_user",
        password="hashed_password",
        first_name="Jane",
        last_name="Smith",
        email="doctor@clinic.com",
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
def basic_admin(test_session):
    user = User(
        username="admin_user",
        password="hashed_password",
        first_name="Super",
        last_name="Admin",
        email="admin@clinic.com",
        is_active=True
    )
    user.role = UserRole.ADMIN
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def basic_appointment(test_session, basic_patient, basic_doctor):
    appointment_date = datetime(2026, 1, 1, 10, 0)
    appointment = Appointment(
        name="General Checkup",
        note="Bệnh nhân cần kiểm tra tổng quát",
        status=StatusRole.PENDING,
        appointment_date=appointment_date,
        doctor_profile_id=basic_doctor.profile.id,
        patient_profile_id=basic_patient.profile.id
    )
    test_session.add(appointment)
    test_session.commit()
    return appointment


class TestValidateRequest:
    def test_request_not_patient(self, basic_doctor):
        data = {"doctorId": 1, "appointmentDate": "2026-01-01 10:00"}
        date_result, doctor_result, error_result = validate_appointment_request(basic_doctor, data)
        assert date_result is None
        assert doctor_result is None
        assert error_result[1] == "FORBIDDEN"

    def test_request_missing_data(self, basic_patient):
        data = {"doctorId": 1}
        date_result, doctor_result, error_result = validate_appointment_request(basic_patient, data)
        assert date_result is None
        assert doctor_result is None
        assert error_result[1] == "ERROR_BAD_REQUEST"

    @patch("src.modules.appointments.services.validate_appointment_booking")
    def test_request_success_flow(self, mock_validate_booking, basic_patient):
        mock_date = datetime(2026, 1, 1, 10, 0)
        mock_doctor = MagicMock()
        mock_validate_booking.return_value = (mock_date, mock_doctor, None)
        data = {"doctorId": 1, "appointmentDate": "2026-01-01 10:00"}

        date_result, doctor_result, error_result = validate_appointment_request(basic_patient, data)
        assert date_result == mock_date
        assert doctor_result == mock_doctor
        assert error_result is None


class TestValidateBooking:
    @patch("src.modules.appointments.services.parse_appointment_datetime")
    def test_booking_parse_error(self, mock_parse):
        mock_parse.return_value = (None, ({"message": "Error"}, "ERROR_BAD_REQUEST"))
        date_result, doctor_result, error_result = validate_appointment_booking(1, "invalid", MagicMock())
        assert error_result[1] == "ERROR_BAD_REQUEST"

    @patch("src.modules.appointments.services.validate_appointment_date")
    @patch("src.modules.appointments.services.parse_appointment_datetime")
    def test_booking_date_error(self, mock_parse, mock_validate_date):
        mock_parse.return_value = (datetime(2020, 1, 1), None)
        mock_validate_date.return_value = ({"message": "Past date"}, "ERROR_BAD_REQUEST")
        date_result, doctor_result, error_result = validate_appointment_booking(1, "2020-01-01", MagicMock())
        assert error_result[1] == "ERROR_BAD_REQUEST"

    @patch("src.modules.appointments.services.validate_doctor")
    @patch("src.modules.appointments.services.get_doctor_by_id")
    @patch("src.modules.appointments.services.validate_appointment_date")
    @patch("src.modules.appointments.services.parse_appointment_datetime")
    def test_booking_doctor_error(self, mock_parse, mock_validate_date, mock_get_doctor, mock_validate_doctor):
        mock_parse.return_value = (datetime(2026, 1, 1), None)
        mock_validate_date.return_value = (None, None)
        mock_get_doctor.return_value = None
        mock_validate_doctor.return_value = ({"message": "Invalid"}, "ERROR_BAD_REQUEST")

        date_result, doctor_result, error_result = validate_appointment_booking(1, "2026-01-01", MagicMock())
        assert error_result[1] == "ERROR_BAD_REQUEST"

    @patch("src.modules.appointments.services.validate_available_slot")
    @patch("src.modules.appointments.services.validate_doctor")
    @patch("src.modules.appointments.services.get_doctor_by_id")
    @patch("src.modules.appointments.services.validate_appointment_date")
    @patch("src.modules.appointments.services.parse_appointment_datetime")
    def test_booking_slot_error(self, mock_parse, mock_validate_date, mock_get_doctor, mock_validate_doctor,
                                mock_validate_slot):
        mock_parse.return_value = (datetime(2026, 1, 1), None)
        mock_validate_date.return_value = (None, None)
        mock_get_doctor.return_value = MagicMock()
        mock_validate_doctor.return_value = (None, None)
        mock_validate_slot.return_value = ({"message": "Slot full"}, "ERROR_BAD_REQUEST")

        date_result, doctor_result, error_result = validate_appointment_booking(1, "2026-01-01", MagicMock())
        assert error_result[1] == "ERROR_BAD_REQUEST"

    @patch("src.modules.appointments.services.validate_available_slot")
    @patch("src.modules.appointments.services.validate_doctor")
    @patch("src.modules.appointments.services.get_doctor_by_id")
    @patch("src.modules.appointments.services.validate_appointment_date")
    @patch("src.modules.appointments.services.parse_appointment_datetime")
    def test_booking_success_flow(self, mock_parse, mock_validate_date, mock_get_doctor, mock_validate_doctor,
                                  mock_validate_slot):
        mock_datetime = datetime(2026, 1, 1)
        mock_doctor = MagicMock()
        mock_parse.return_value = (mock_datetime, None)
        mock_validate_date.return_value = (None, None)
        mock_get_doctor.return_value = mock_doctor
        mock_validate_doctor.return_value = (None, None)
        mock_validate_slot.return_value = (None, None)

        date_result, doctor_result, error_result = validate_appointment_booking(1, "2026-01-01", MagicMock())
        assert error_result is None
        assert date_result == mock_datetime
        assert doctor_result == mock_doctor


class TestGetAppointmentList:
    def test_list_patient_role(self, basic_appointment, basic_patient, test_app):
        with test_app.app_context():
            result, status = get_appointments_list_service(basic_patient, 1, 10)
            assert status == "SUCCESS"
            assert result["meta"]["total"] == 1

    def test_list_doctor_role(self, basic_appointment, basic_doctor, test_app):
        with test_app.app_context():
            result, status = get_appointments_list_service(basic_doctor, 1, 10)
            assert status == "SUCCESS"
            assert result["meta"]["total"] == 1

    def test_list_admin_role(self, basic_appointment, basic_admin, test_app):
        with test_app.app_context():
            result, status = get_appointments_list_service(basic_admin, 1, 10)
            assert status == "SUCCESS"
            assert result["meta"]["total"] == 1

    def test_list_invalid_role(self, test_app):
        mock_user = MagicMock()
        mock_user.role.name = "UNKNOWN"
        with test_app.app_context():
            result, status = get_appointments_list_service(mock_user, 1, 10)
            assert status == "FORBIDDEN"


class TestGetAppointmentDetail:
    def test_detail_not_found(self, basic_patient, test_app):
        with test_app.app_context():
            result, status = get_appointment_detail_service(basic_patient, 999)
            assert status == "NOT_FOUND"

    def test_detail_forbidden(self, basic_appointment, test_app, test_session):
        other_patient = User(
            username="other",
            password="hashed_password",
            first_name="Other",
            last_name="Patient",
            email="other@clinic.com",
            role=UserRole.PATIENT
        )
        test_session.add(other_patient)
        test_session.flush()
        other_profile = PatientProfile(user_id=other_patient.id)
        test_session.add(other_profile)
        test_session.commit()

        with test_app.app_context():
            result, status = get_appointment_detail_service(other_patient, basic_appointment.id)
            assert status == "FORBIDDEN"

    @patch("src.modules.appointments.services.format_appointment_summary")
    def test_detail_success_flow(self, mock_format, basic_appointment, basic_patient, test_app):
        mock_format.return_value = {"summary": "Detail Data"}
        with test_app.app_context():
            result, status = get_appointment_detail_service(basic_patient, basic_appointment.id)
            assert status == "SUCCESS"
            assert result["summary"] == "Detail Data"


class TestCreatePatientAppointment:
    @patch("src.modules.appointments.services.validate_appointment_request")
    def test_patient_create_error(self, mock_validate, basic_patient, test_app):
        mock_validate.return_value = (None, None, ({"message": "Error"}, "ERROR_BAD_REQUEST"))
        with test_app.app_context():
            result = create_patient_appointment_service(basic_patient, {})
            assert result[1] == "ERROR_BAD_REQUEST"

    @patch("src.modules.appointments.services.format_appointment_response")
    @patch("src.modules.appointments.services.validate_appointment_request")
    def test_patient_create_success(self, mock_validate, mock_format, basic_patient, basic_doctor, test_app,
                                    test_session):
        mock_validate.return_value = (datetime(2026, 1, 1), basic_doctor, None)
        mock_format.return_value = {"id": 1}
        with test_app.app_context():
            result, status = create_patient_appointment_service(basic_patient, {})
            assert status == "SUCCESS"
            assert result["id"] == 1
            new_appointment = test_session.query(Appointment).filter_by(
                patient_profile_id=basic_patient.profile.id).first()
            assert new_appointment is not None


class TestCreateReceptionistAppointment:
    def test_reception_create_error(self, basic_patient, test_app):
        with test_app.app_context():
            result, status = create_receptionist_appointment_service(basic_patient, {})
            assert status == "FORBIDDEN"

    @patch("src.modules.appointments.services.format_appointment_response")
    @patch("src.modules.appointments.services.get_or_create_patient")
    @patch("src.modules.appointments.services.validate_appointment_booking")
    def test_reception_create_success(self, mock_validate_booking, mock_get_patient, mock_format, basic_admin,
                                      basic_patient, basic_doctor, test_app, test_session):
        mock_validate_booking.return_value = (datetime(2026, 1, 1), basic_doctor, None)
        mock_get_patient.return_value = (basic_patient.profile, None)
        mock_format.return_value = {"id": 2}

        data = {"lastName": "Doe", "firstName": "John"}
        with test_app.app_context():
            result, status = create_receptionist_appointment_service(basic_admin, data)
            assert status == "SUCCESS"
            assert result["id"] == 2


class TestPatchAppointment:
    def test_patch_role_forbidden(self, basic_appointment, basic_patient, test_app):
        with test_app.app_context():
            result, status = patch_appointment_service(basic_patient, basic_appointment.id, {})
            assert status == "FORBIDDEN"

    def test_patch_not_found(self, basic_admin, test_app):
        with test_app.app_context():
            result, status = patch_appointment_service(basic_admin, 999, {})
            assert status == "NOT_FOUND"

    def test_patch_success_flow(self, basic_appointment, basic_admin, test_app, test_session):
        with test_app.app_context():
            data = {"note": "Updated note", "status": "APPROVED"}
            result, status = patch_appointment_service(basic_admin, basic_appointment.id, data)
            assert status == "SUCCESS"

            updated_appointment = test_session.get(Appointment, basic_appointment.id)
            assert updated_appointment.note == "Updated note"
            assert updated_appointment.status == StatusRole.APPROVED


class TestDeleteAppointment:
    def test_delete_role_forbidden(self, basic_appointment, basic_patient, test_app):
        with test_app.app_context():
            result, status = delete_appointment_service(basic_patient, basic_appointment.id)
            assert status == "FORBIDDEN"

    def test_delete_status_error(self, basic_appointment, basic_admin, test_app):
        with test_app.app_context():
            result, status = delete_appointment_service(basic_admin, basic_appointment.id)
            assert status == "ERROR_BAD_REQUEST"

    def test_delete_success_flow(self, basic_appointment, basic_admin, test_app, test_session):
        basic_appointment.status = StatusRole.CANCEL
        test_session.commit()
        with test_app.app_context():
            result, status = delete_appointment_service(basic_admin, basic_appointment.id)
            assert status == "SUCCESS"
            assert test_session.get(Appointment, basic_appointment.id) is None


class TestHandleDateUpdate:
    def test_date_update_empty(self, basic_appointment):
        result = handle_date_update(basic_appointment, None)
        assert result is None

    @patch("src.modules.appointments.services.validate_available_slot")
    @patch("src.modules.appointments.services.get_available_time_slots")
    @patch("src.modules.appointments.services.validate_appointment_date")
    @patch("src.modules.appointments.services.parse_appointment_datetime")
    def test_date_update_fail(self, mock_parse, mock_validate_date, mock_get_slots, mock_validate_slot,
                              basic_appointment):
        mock_parse.return_value = (datetime(2026, 2, 2), None)
        mock_validate_date.return_value = (None, None)
        mock_get_slots.return_value = []
        mock_validate_slot.return_value = ({"message": "Full"}, "ERROR_BAD_REQUEST")

        result = handle_date_update(basic_appointment, "2026-02-02")
        assert result[1] == "ERROR_BAD_REQUEST"

    @patch("src.modules.appointments.services.validate_available_slot")
    @patch("src.modules.appointments.services.get_available_time_slots")
    @patch("src.modules.appointments.services.validate_appointment_date")
    @patch("src.modules.appointments.services.parse_appointment_datetime")
    def test_date_update_success(self, mock_parse, mock_validate_date, mock_get_slots, mock_validate_slot,
                                 basic_appointment):
        new_date = datetime(2026, 2, 2)
        mock_parse.return_value = (new_date, None)
        mock_validate_date.return_value = (None, None)
        mock_get_slots.return_value = []
        mock_validate_slot.return_value = (None, None)

        result = handle_date_update(basic_appointment, "2026-02-02")
        assert result is None
        assert basic_appointment.appointment_date == new_date


class TestGetPatientProfile:
    def test_profile_role_forbidden(self, basic_appointment, basic_patient, test_app):
        with test_app.app_context():
            result, status = get_patient_profile_service(basic_patient, basic_appointment.id)
            assert status == "FORBIDDEN"

    def test_profile_success_flow(self, basic_appointment, basic_doctor, test_app):
        with test_app.app_context():
            result, status = get_patient_profile_service(basic_doctor, basic_appointment.id)
            assert status == "SUCCESS"
            assert result["firstName"] == "John"


class TestHandleStatusUpdate:
    def test_status_update_valid(self, basic_appointment):
        result = handle_status_update(basic_appointment, "COMPLETED")
        assert result is None
        assert basic_appointment.status == StatusRole.COMPLETED

    def test_status_update_invalid(self, basic_appointment):
        result = handle_status_update(basic_appointment, "INVALID_STATUS")
        assert result[1] == "ERROR_BAD_REQUEST"


class TestGetOrCreatePatient:
    def test_create_patient_invalid(self):
        data = {"birthday": "wrong_date", "gender": "UNKNOWN"}
        result, error = get_or_create_patient(data)
        assert result is None
        assert error[1] == "ERROR_BAD_REQUEST"

    def test_create_patient_success(self, test_app):
        data = {
            "firstName": "New",
            "lastName": "Patient",
            "phone": "999888777",
            "gender": "MALE",
            "birthday": "1995-05-05",
            "address": "456 Avenue"
        }
        with test_app.app_context():
            profile, error = get_or_create_patient(data)
            assert error is None
            assert profile.phone == "999888777"


class TestValidateDoctor:
    def test_doctor_invalid_flow(self, basic_patient):
        error, status = validate_doctor(None)
        assert status == "ERROR_BAD_REQUEST"

        error, status = validate_doctor(basic_patient)
        assert status == "ERROR_BAD_REQUEST"

    def test_doctor_valid_flow(self, basic_doctor):
        error, status = validate_doctor(basic_doctor)
        assert error is None
        assert status is None
