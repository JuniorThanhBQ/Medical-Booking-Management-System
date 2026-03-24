from datetime import time
from unittest.mock import MagicMock, patch

from tests.test_base import test_app, test_session


class MockRole:
    def __init__(self, name):
        self.name = name


class MockUser:
    def __init__(self, role_name, profile_type="doctor", has_profile=True, has_ws=False):
        self.role = MockRole(role_name)
        if has_profile:
            self.profile = MagicMock()
            self.profile.profile_type = profile_type
            self.profile.id = 1
            self.profile.specialty = MagicMock()
            if has_ws:
                self.profile.work_schedule = MagicMock()
                self.profile.work_schedule.title = "Morning Shift"
                self.profile.work_schedule.description = "Regular checkups"
                self.profile.work_schedule.start_time = time(8, 0, 0)
                self.profile.work_schedule.end_time = time(12, 0, 0)

                wd1, wd2, wd3 = MagicMock(), MagicMock(), MagicMock()
                wd1.day_of_week.name = "MONDAY"
                wd2.day_of_week.name = "WEDNESDAY"
                wd3.day_of_week.name = "FRIDAY"
                self.profile.work_schedule.work_dates = [wd1, wd2, wd3]
            else:
                self.profile.work_schedule = None
        else:
            self.profile = None


class TestGetDoctorSchedule:
    @patch("src.modules.doctor.services.Appointment.query")
    @patch("src.modules.doctor.services.format_appointment_summary")
    def test_successfully_retrieve_schedule_and_upcoming_appointments(self, mock_format, mock_query, test_app,
                                                                      test_session):
        from src.modules.doctor.services import get_my_schedule_service

        doctor_user = MockUser("DOCTOR", has_profile=True, has_ws=True)
        mock_appointment = MagicMock()
        mock_query.filter.return_value.order_by.return_value.all.return_value = [mock_appointment]
        mock_format.return_value = {"status": "APPROVED"}

        result, status = get_my_schedule_service(doctor_user)

        assert status == "SUCCESS"
        assert result["workSchedule"]["title"] == "Morning Shift"
        assert result["workSchedule"]["startTime"] == "08:00:00"
        assert result["workSchedule"]["workDate"] == ["Monday", "Wednesday", "Friday"]
        assert len(result["appointments"]) == 1
        assert result["appointments"][0]["status"] == "APPROVED"

    @patch("src.modules.doctor.services.Appointment.query")
    def test_retrieve_schedule_when_none_exists(self, mock_query, test_app, test_session):
        from src.modules.doctor.services import get_my_schedule_service

        doctor_user = MockUser("DOCTOR", has_profile=True, has_ws=False)
        mock_query.filter.return_value.order_by.return_value.all.return_value = []

        result, status = get_my_schedule_service(doctor_user)

        assert status == "SUCCESS"
        assert result["workSchedule"] is None
        assert result["appointments"] == []

    def test_fail_retrieval_for_non_doctor_role(self, test_app, test_session):
        from src.modules.doctor.services import get_my_schedule_service

        patient_user = MockUser("PATIENT")

        result, status = get_my_schedule_service(patient_user)

        assert status == "FORBIDDEN"
        assert result["message"] == "Chỉ bác sĩ mới có quyền truy cập"

    def test_fail_retrieval_for_doctor_missing_valid_profile(self, test_app, test_session):
        from src.modules.doctor.services import get_my_schedule_service

        doctor_user = MockUser("DOCTOR", has_profile=False)

        result, status = get_my_schedule_service(doctor_user)

        assert status == "NOT_FOUND"
        assert result["message"] == "Hồ sơ bác sĩ không hợp lệ"


class TestRequestScheduleChange:
    @patch("src.modules.doctor.services.Appointment.query")
    @patch("src.modules.doctor.services.WorkDate.query")
    @patch("src.modules.doctor.services.db.session")
    def test_successfully_update_schedule_with_no_conflicts(self, mock_session, mock_wd_query, mock_app_query, test_app,
                                                            test_session):
        from src.modules.doctor.services import request_schedule_change_service

        doctor_user = MockUser("DOCTOR", has_profile=True, has_ws=True)
        mock_app_query.filter.return_value.first.return_value = None
        data = {
            "newWorkSchedule": {
                "title": "New Shift",
                "description": "Updated hours",
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "work_date": ["MONDAY", "TUESDAY"]
            }
        }

        result, status = request_schedule_change_service(doctor_user, data)

        assert status == "SUCCESS"
        assert result["message"] == "Đã gửi yêu cầu đổi lịch"
        mock_wd_query.filter_by.return_value.delete.assert_called_once()
        mock_session.flush.assert_called_once()
        mock_session.commit.assert_called_once()
        assert doctor_user.profile.work_schedule.start_time == time(9, 0, 0)
        assert doctor_user.profile.work_schedule.end_time == time(17, 0, 0)

    @patch("src.modules.doctor.services.Appointment.query")
    def test_fail_schedule_update_due_to_upcoming_appointments(self, mock_app_query, test_app, test_session):
        from src.modules.doctor.services import request_schedule_change_service

        doctor_user = MockUser("DOCTOR", has_profile=True, has_ws=True)
        mock_app_query.filter.return_value.first.return_value = MagicMock()
        data = {
            "newWorkSchedule": {
                "start_time": "08:00:00",
                "end_time": "12:00:00"
            }
        }

        result, status = request_schedule_change_service(doctor_user, data)

        assert status == "FORBIDDEN"
        assert result["message"] == "Có lịch hẹn ở trong phạm vi 7 ngày tới."

    @patch("src.modules.doctor.services.Appointment.query")
    def test_fail_schedule_update_due_to_invalid_time_format(self, mock_app_query, test_app, test_session):
        from src.modules.doctor.services import request_schedule_change_service

        doctor_user = MockUser("DOCTOR", has_profile=True, has_ws=True)
        mock_app_query.filter.return_value.first.return_value = None
        data = {
            "newWorkSchedule": {
                "start_time": "9 AM",
                "end_time": "25:00:00"
            }
        }

        result, status = request_schedule_change_service(doctor_user, data)

        assert status == "ERROR_BAD_REQUEST"
        assert result["message"] == "Định dạng không hợp lệ (HH:MM:SS)"

    @patch("src.modules.doctor.services.Appointment.query")
    def test_fail_schedule_update_missing_payload_data(self, mock_app_query, test_app, test_session):
        from src.modules.doctor.services import request_schedule_change_service

        doctor_user = MockUser("DOCTOR", has_profile=True, has_ws=True)
        mock_app_query.filter.return_value.first.return_value = None

        result, status = request_schedule_change_service(doctor_user, {})

        assert status == "ERROR_BAD_REQUEST"
        assert result["message"] == "Thiếu thông tin lịch làm việc mới"

    @patch("src.modules.doctor.services.Appointment.query")
    @patch("src.modules.doctor.services.WorkDate.query")
    @patch("src.modules.doctor.services.db.session")
    def test_successfully_create_schedule_and_ignore_invalid_days(self, mock_session, mock_wd_query, mock_app_query,
                                                                  test_app, test_session):
        from src.modules.doctor.services import request_schedule_change_service

        doctor_user = MockUser("DOCTOR", has_profile=True, has_ws=False)
        mock_app_query.filter.return_value.first.return_value = None
        data = {
            "newWorkSchedule": {
                "start_time": "08:00:00",
                "end_time": "16:00:00",
                "work_date": ["MONDAY", "INVALID_DAY", "FRIDAY"]
            }
        }

        result, status = request_schedule_change_service(doctor_user, data)

        assert status == "SUCCESS"
        assert result["message"] == "Đã gửi yêu cầu đổi lịch"
        mock_session.add.assert_called()
        mock_session.commit.assert_called_once()

    def test_fail_schedule_update_for_non_doctor(self, test_app, test_session):
        from src.modules.doctor.services import request_schedule_change_service

        receptionist_user = MockUser("RECEPTIONIST")
        data = {
            "newWorkSchedule": {
                "start_time": "08:00:00",
                "end_time": "17:00:00"
            }
        }

        result, status = request_schedule_change_service(receptionist_user, data)

        assert status == "FORBIDDEN"
        assert result["message"] == "Chỉ bác sĩ mới có quyền này"
