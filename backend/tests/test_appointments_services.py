from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

from src.modules.appointments.models import StatusRole
from src.modules.appointments.services import (
    create_patient_appointment_service, delete_appointment_service,
    get_appointment_detail_service, get_appointments_list_service,
    get_patient_profile_service, parse_appointment_datetime,
    patch_appointment_service, validate_appointment_date,
    validate_available_slot, validate_doctor)
from tests.test_base import test_app, test_session


class MockRole:
    def __init__(self, name):
        self.name = name


class MockSpecialty:
    def __init__(self, name="General"):
        self.id = 1
        self.name = name
        self.cta_label = MagicMock()
        self.cta_label.name = "CTA"


class MockUser:
    def __init__(self, role_name, profile_id=None, user_id=1, first_name="John", last_name="Doe", is_active=True):
        self.id = user_id
        self.role = MockRole(role_name)
        self.first_name = first_name
        self.last_name = last_name
        self.is_active = is_active
        self.profile = MagicMock(id=profile_id) if profile_id else None


class MockPatient:
    def __init__(self):
        self.user = MockUser("PATIENT", first_name="John", last_name="Doe")
        self.birthday = datetime(1990, 1, 1)
        self.gender = MockRole("MALE")
        self.phone = "0987654321"
        self.address = "123 Main St"
        self.avatar = "avatar.png"
        self.medical_history = "None"


class MockDoctor:
    def __init__(self):
        self.user = MockUser("DOCTOR", first_name="Jane", last_name="Smith")
        self.specialty = MockSpecialty()


class TestGetAppointmentsList:
    @patch("src.modules.appointments.services.Appointment.query")
    def test_admin_retrieves_paginated_appointments_list(self, mock_query, test_app):
        admin_user = MockUser("ADMIN")

        mock_appointment = MagicMock()
        mock_appointment.id = 1
        mock_appointment.doctor = MockDoctor()
        mock_appointment.patient = MockPatient()
        mock_appointment.status.name = "APPROVED"
        mock_appointment.appointment_date = datetime(2026, 3, 24, 10, 0, 0)

        mock_pagination = MagicMock()
        mock_pagination.items = [mock_appointment]
        mock_pagination.total = 1
        mock_pagination.pages = 1
        mock_pagination.page = 1
        mock_pagination.per_page = 10
        mock_pagination.has_next = False
        mock_pagination.has_prev = False

        mock_query.order_by.return_value.paginate.return_value = mock_pagination

        result, status = get_appointments_list_service(admin_user, 1, 10)

        assert status == "SUCCESS"
        assert len(result["items"]) == 1
        assert result["items"][0]["id"] == "1"
        assert result["items"][0]["patientName"] == "Doe John"
        assert result["meta"]["total"] == 1

    @patch("src.modules.appointments.services.Appointment.query")
    def test_patient_retrieves_their_own_appointments(self, mock_query, test_app):
        patient_user = MockUser("PATIENT", profile_id=5)

        mock_pagination = MagicMock()
        mock_pagination.items = []
        mock_query.filter.return_value.order_by.return_value.paginate.return_value = mock_pagination

        result, status = get_appointments_list_service(patient_user, 1, 10)

        assert status == "SUCCESS"
        assert len(result["items"]) == 0
        mock_query.filter.assert_called_once()

    @patch("src.modules.appointments.services.Appointment.query")
    def test_patient_without_profile_retrieves_appointments(self, mock_query, test_app):
        patient_user = MockUser("PATIENT", profile_id=None)

        result, status = get_appointments_list_service(patient_user, 1, 10)

        assert status == "SUCCESS"
        assert len(result["items"]) == 0
        assert result["meta"]["total"] == 0

    @patch("src.modules.appointments.services.Appointment.query")
    def test_unauthorized_role_attempts_access(self, mock_query, test_app):
        invalid_user = MockUser("INVALID_ROLE")

        result, status = get_appointments_list_service(invalid_user, 1, 10)

        assert status == "FORBIDDEN"
        assert result["message"] == "Không có quyền truy cập"


class TestGetAppointmentDetail:
    @patch("src.modules.appointments.services.db.session.get")
    @patch("src.modules.appointments.services.format_appointment_summary")
    def test_doctor_retrieves_their_own_appointment_detail(self, mock_format, mock_get):
        doctor_user = MockUser("DOCTOR", profile_id=2)
        mock_appointment = MagicMock(doctor_profile_id=2, medical_record_id=500)
        mock_appointment.doctor = MockDoctor()
        mock_appointment.patient = MockPatient()
        mock_get.return_value = mock_appointment
        mock_format.return_value = {"status": "APPROVED"}

        result, status = get_appointment_detail_service(doctor_user, 100)

        assert status == "SUCCESS"
        assert result["medicalRecordId"] == "500"
        assert result["status"] == "APPROVED"

    @patch("src.modules.appointments.services.db.session.get")
    def test_patient_forbidden_from_viewing_another_patients_appointment(self, mock_get):
        patient_user = MockUser("PATIENT", profile_id=5)
        mock_appointment = MagicMock(patient_profile_id=10)
        mock_get.return_value = mock_appointment

        result, status = get_appointment_detail_service(patient_user, 101)

        assert status == "FORBIDDEN"
        assert result["message"] == "Không có quyền truy cập"

    @patch("src.modules.appointments.services.db.session.get")
    def test_retrieve_non_existent_appointment(self, mock_get):
        receptionist_user = MockUser("RECEPTIONIST")
        mock_get.return_value = None

        result, status = get_appointment_detail_service(receptionist_user, 9999)

        assert status == "NOT_FOUND"
        assert result["message"] == "Lịch hẹn không tồn tại"


class TestGetPatientProfileViaAppointment:
    @patch("src.modules.appointments.services.db.session.get")
    def test_doctor_successfully_retrieves_patient_profile(self, mock_get):
        doctor_user = MockUser("DOCTOR", profile_id=2)
        mock_appointment = MagicMock(doctor_profile_id=2)
        mock_appointment.patient = MockPatient()
        mock_get.return_value = mock_appointment

        result, status = get_patient_profile_service(doctor_user, 100)

        assert status == "SUCCESS"
        assert result["firstName"] == "John"
        assert result["phone"] == "0987654321"

    @patch("src.modules.appointments.services.db.session.get")
    def test_doctor_forbidden_from_viewing_another_doctors_patient(self, mock_get):
        doctor_user = MockUser("DOCTOR", profile_id=3)
        mock_appointment = MagicMock(doctor_profile_id=2)
        mock_get.return_value = mock_appointment

        result, status = get_patient_profile_service(doctor_user, 100)

        assert status == "FORBIDDEN"
        assert result["message"] == "Không có quyền trên lịch hẹn này"

    def test_non_doctor_role_attempts_to_access_patient_profile(self):
        receptionist_user = MockUser("RECEPTIONIST")

        result, status = get_patient_profile_service(receptionist_user, 100)

        assert status == "FORBIDDEN"
        assert result["message"] == "Chỉ bác sĩ mới có quyền này"


class TestCreatePatientAppointment:
    @patch("src.modules.appointments.services.validate_appointment_booking")
    @patch("src.modules.appointments.services.db.session.add")
    @patch("src.modules.appointments.services.db.session.commit")
    @patch("src.modules.appointments.services.format_appointment_response")
    def test_successful_appointment_creation(self, mock_format, mock_commit, mock_add, mock_validate):
        patient_user = MockUser("PATIENT", profile_id=5)
        data = {"doctorId": 10, "appointmentDate": "2026-03-25T14:30:00Z", "note": "Routine checkup"}

        mock_doctor = MockUser("DOCTOR", profile_id=10)
        mock_dt = datetime(2026, 3, 25, 14, 30, 0)
        mock_validate.return_value = (mock_dt, mock_doctor, None)
        mock_format.return_value = {"appointmentId": "generated_id", "status": "APPROVED"}

        result, status = create_patient_appointment_service(patient_user, data)

        assert status == "SUCCESS"
        assert result["appointmentId"] == "generated_id"
        mock_add.assert_called_once()
        mock_commit.assert_called_once()

    @patch("src.modules.appointments.services.validate_appointment_booking")
    def test_booking_fails_for_past_date(self, mock_validate):
        patient_user = MockUser("PATIENT", profile_id=5)
        data = {"doctorId": 10, "appointmentDate": "2025-01-01T10:00:00Z"}

        mock_validate.return_value = (None, None,
                                      ({"message": "Chỉ được đặt lịch trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"))

        result, status = create_patient_appointment_service(patient_user, data)

        assert status == "ERROR_BAD_REQUEST"
        assert result["message"] == "Chỉ được đặt lịch trong vòng 7 ngày tới"

    @patch("src.modules.appointments.services.validate_appointment_booking")
    def test_booking_fails_for_date_beyond_7_days(self, mock_validate):
        patient_user = MockUser("PATIENT", profile_id=5)
        data = {"doctorId": 10, "appointmentDate": "2026-04-01T10:00:00Z"}

        mock_validate.return_value = (None, None,
                                      ({"message": "Chỉ được đặt lịch trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"))

        result, status = create_patient_appointment_service(patient_user, data)

        assert status == "ERROR_BAD_REQUEST"
        assert result["message"] == "Chỉ được đặt lịch trong vòng 7 ngày tới"

    @patch("src.modules.appointments.services.validate_appointment_booking")
    def test_booking_fails_for_unavailable_slot(self, mock_validate):
        patient_user = MockUser("PATIENT", profile_id=5)
        data = {"doctorId": 10, "appointmentDate": "2026-03-25T14:30:00Z"}

        mock_validate.return_value = (None, None, ({"message": "Khung giờ này không khả dụng hoặc đã có người đặt"},
                                                   "ERROR_BAD_REQUEST"))

        result, status = create_patient_appointment_service(patient_user, data)

        assert status == "ERROR_BAD_REQUEST"
        assert result["message"] == "Khung giờ này không khả dụng hoặc đã có người đặt"

    @patch("src.modules.appointments.services.validate_appointment_booking")
    def test_booking_fails_for_inactive_or_invalid_doctor(self, mock_validate):
        patient_user = MockUser("PATIENT", profile_id=5)
        data = {"doctorId": 99, "appointmentDate": "2026-03-25T14:30:00Z"}

        mock_validate.return_value = (None, None, ({"message": "Bác sĩ không hợp lệ"}, "ERROR_BAD_REQUEST"))

        result, status = create_patient_appointment_service(patient_user, data)

        assert status == "ERROR_BAD_REQUEST"
        assert result["message"] == "Bác sĩ không hợp lệ"


class TestPatchAppointment:
    @patch("src.modules.appointments.services.db.session.get")
    @patch("src.modules.appointments.services.db.session.commit")
    def test_receptionist_successfully_updates_status_and_note(self, mock_commit, mock_get):
        receptionist_user = MockUser("RECEPTIONIST")
        mock_appointment = MagicMock()
        mock_get.return_value = mock_appointment
        data = {"status": "CANCEL", "note": "Patient requested cancellation"}

        result, status = patch_appointment_service(receptionist_user, 100, data)

        assert status == "SUCCESS"
        assert mock_appointment.status == StatusRole.CANCEL
        assert mock_appointment.note == "Patient requested cancellation"
        mock_commit.assert_called_once()

    @patch("src.modules.appointments.services.db.session.get")
    @patch("src.modules.appointments.services.db.session.commit")
    @patch("src.modules.appointments.services.get_available_time_slots")
    def test_admin_successfully_reschedules_appointment(self, mock_get_slots, mock_commit, mock_get):
        admin_user = MockUser("ADMIN")
        mock_appointment = MagicMock()
        mock_appointment.appointment_date = datetime(2026, 3, 25, 10, 0, 0)
        mock_appointment.doctor.user = MockUser("DOCTOR")
        mock_get.return_value = mock_appointment

        mock_get_slots.return_value = ["2026-03-26T10:00:00Z"]
        data = {"appointmentDate": "2026-03-26T10:00:00Z", "note": "Rescheduled"}

        result, status = patch_appointment_service(admin_user, 100, data)

        assert status == "SUCCESS"
        assert mock_appointment.appointment_date == datetime(2026, 3, 26, 10, 0, 0)
        mock_commit.assert_called_once()

    @patch("src.modules.appointments.services.db.session.get")
    def test_update_fails_with_invalid_status(self, mock_get):
        receptionist_user = MockUser("RECEPTIONIST")
        mock_get.return_value = MagicMock()
        data = {"status": "INVALID_STATUS", "note": "test"}

        result, status = patch_appointment_service(receptionist_user, 100, data)

        assert status == "ERROR_BAD_REQUEST"
        assert result["message"] == "Trạng thái không hợp lệ"

    def test_patient_forbidden_from_patching_appointment(self):
        patient_user = MockUser("PATIENT")
        data = {"status": "CANCEL"}

        result, status = patch_appointment_service(patient_user, 100, data)

        assert status == "FORBIDDEN"
        assert result["message"] == "Không có quyền thực hiện"


class TestDeleteAppointment:
    @patch("src.modules.appointments.services.db.session.get")
    @patch("src.modules.appointments.services.db.session.delete")
    @patch("src.modules.appointments.services.db.session.commit")
    def test_admin_successfully_deletes_a_cancelled_appointment(self, mock_commit, mock_delete, mock_get):
        admin_user = MockUser("ADMIN")
        mock_appointment = MagicMock(status=StatusRole.CANCEL)
        mock_get.return_value = mock_appointment

        result, status = delete_appointment_service(admin_user, 200)

        assert status == "SUCCESS"
        mock_delete.assert_called_once_with(mock_appointment)
        mock_commit.assert_called_once()

    @patch("src.modules.appointments.services.db.session.get")
    def test_deletion_fails_for_non_cancelled_appointment(self, mock_get):
        receptionist_user = MockUser("RECEPTIONIST")
        mock_appointment = MagicMock(status=StatusRole.APPROVED)
        mock_get.return_value = mock_appointment

        result, status = delete_appointment_service(receptionist_user, 100)

        assert status == "ERROR_BAD_REQUEST"
        assert result["message"] == "Chỉ được phép xóa lịch hẹn ở trạng thái đã hủy"

    def test_doctor_forbidden_from_deleting_appointment(self):
        doctor_user = MockUser("DOCTOR")

        result, status = delete_appointment_service(doctor_user, 200)

        assert status == "FORBIDDEN"
        assert result["message"] == "Không có quyền thực hiện"


class TestValidationUtils:
    def test_parse_appointment_datetime(self):
        dt, err = parse_appointment_datetime("2026-03-24T10:00:00Z")
        assert dt == datetime(2026, 3, 24, 10, 0, 0)
        assert err is None

        dt, err = parse_appointment_datetime("invalid-date")
        assert dt is None
        assert err[0]["message"] == "Định dạng ngày không hợp lệ"

    def test_validate_appointment_date(self):
        valid_dt = datetime.now() + timedelta(days=2)
        err, status = validate_appointment_date(valid_dt)
        assert err is None

        past_dt = datetime.now() - timedelta(days=1)
        err, status = validate_appointment_date(past_dt)
        assert err["message"] == "Chỉ được đặt lịch trong vòng 7 ngày tới"

    def test_validate_doctor(self):
        valid_doctor = MockUser("DOCTOR", is_active=True)
        err, status = validate_doctor(valid_doctor)
        assert err is None

        invalid_doctor = MockUser("PATIENT")
        err, status = validate_doctor(invalid_doctor)
        assert err["message"] == "Bác sĩ không hợp lệ"

    def test_validate_available_slot(self):
        dt = datetime(2026, 3, 25, 10, 0, 0)
        available = ["2026-03-25T10:00:00Z"]
        err, status = validate_available_slot(dt, available)
        assert err is None

        err, status = validate_available_slot(dt, [])
        assert err["message"] == "Khung giờ này không khả dụng hoặc đã có người đặt"
