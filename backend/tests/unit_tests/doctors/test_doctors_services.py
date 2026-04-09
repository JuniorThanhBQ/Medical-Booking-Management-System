from datetime import datetime, time, timedelta
from unittest.mock import MagicMock, patch

import pytest

from src.modules.appointments.models import Appointment, StatusRole
from src.modules.doctors.models import DoctorProfile, Specialty, WorkSchedule
from src.modules.doctors.services import (get_my_schedule_service,
                                          request_schedule_change_service)
from src.modules.users.models import PatientProfile, User, UserRole
from tests.test_base import test_app, test_session


@pytest.fixture
def setup_patient_data(test_session):
    user = User(
        username="patient_test",
        password="hashed_password",
        email="patient@test.com",
        first_name="John",
        last_name="Smith",
        is_active=True
    )
    user.role = UserRole.PATIENT
    test_session.add(user)
    test_session.flush()

    profile = PatientProfile(user_id=user.id)
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def doctor_user_setup(test_session):
    user = User(
        username="doctor_test",
        password="hashed_password",
        email="doctor@test.com",
        first_name="Jane",
        last_name="Doe",
        is_active=True
    )
    user.role = UserRole.DOCTOR
    test_session.add(user)
    test_session.flush()

    specialty = Specialty(name="General", level="1")
    test_session.add(specialty)
    test_session.flush()

    profile = DoctorProfile(
        title="Good man",
        bio="Good doctor",
        user_id=user.id,
        specialty_id=specialty.id
    )
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def appointment_setup(test_session, doctor_user_setup, setup_patient_data):
    appointment = Appointment(
        name="Test Appointment",
        note="Routine check",
        appointment_date=datetime.now() + timedelta(days=2),
        doctor_profile_id=doctor_user_setup.profile.id,
        patient_profile_id=setup_patient_data.profile.id,
        status=StatusRole.APPROVED
    )
    test_session.add(appointment)
    test_session.commit()
    return appointment


class TestGetMySchedule:
    def test_get_schedule_not_doctor(self, test_app):
        mock_user = MagicMock()
        mock_user.role.name = "PATIENT"
        with test_app.app_context():
            result, status = get_my_schedule_service(mock_user)
            assert status == "FORBIDDEN"

    def test_get_schedule_no_profile(self, test_app, test_session):
        user = User(username="nodoc", password="1", email="n@d.com", first_name="A", last_name="B")
        user.role = UserRole.DOCTOR
        test_session.add(user)
        test_session.commit()
        with test_app.app_context():
            result, status = get_my_schedule_service(user)
            assert status == "NOT_FOUND"

    def test_get_schedule_empty_work_schedule(self, test_app, doctor_user_setup):
        with test_app.app_context():
            result, status = get_my_schedule_service(doctor_user_setup)
            assert status == "SUCCESS"
            assert result["workSchedule"] is None

    @patch("src.modules.doctors.services.format_appointment_summary")
    def test_get_schedule_success_flow(self, mock_format, test_app, test_session,
                                       doctor_user_setup, appointment_setup):
        mock_format.return_value = {"id": appointment_setup.id}
        schedule = WorkSchedule(
            title="Morning",
            start_time=time(8, 0),
            end_time=time(12, 0),
            doctor_id=doctor_user_setup.profile.id
        )
        test_session.add(schedule)
        test_session.commit()

        with test_app.app_context():
            result, status = get_my_schedule_service(doctor_user_setup)
            assert status == "SUCCESS"
            assert result["workSchedule"]["title"] == "Morning"
            assert len(result["appointments"]) > 0


class TestRequestScheduleChange:
    def test_request_change_not_doctor(self, test_app):
        mock_user = MagicMock()
        mock_user.role.name = "ADMIN"
        with test_app.app_context():
            result, status = request_schedule_change_service(mock_user, {})
            assert status == "FORBIDDEN"

    def test_request_change_has_conflict(self, test_app, doctor_user_setup, appointment_setup):
        with test_app.app_context():
            result, status = request_schedule_change_service(doctor_user_setup, {})
            assert status == "FORBIDDEN"
            assert "7 ngày" in result["message"]

    def test_request_change_no_data(self, test_app, test_session, doctor_user_setup):
        with test_app.app_context():
            result, status = request_schedule_change_service(doctor_user_setup, {})
            assert status == "ERROR_BAD_REQUEST"

    def test_request_change_time_error(self, test_app, doctor_user_setup):
        data = {"newWorkSchedule": {"start_time": "invalid", "end_time": "09:00:00"}}
        with test_app.app_context():
            result, status = request_schedule_change_service(doctor_user_setup, data)
            assert status == "ERROR_BAD_REQUEST"
