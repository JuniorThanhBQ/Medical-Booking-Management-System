from datetime import date, datetime, timedelta
from unittest.mock import MagicMock, patch

from src.modules.doctors.services import (get_medical_service_detail_service,
                                          get_my_schedule_service,
                                          get_specialty_detail_service,
                                          get_time_slots_service,
                                          is_valid_working_day,
                                          parse_and_validate_date,
                                          request_schedule_change_service)


def test_parse_and_validate_date():
    today = date.today()
    dt, err = parse_and_validate_date(None)
    assert dt == today
    assert err is None

    dt, err = parse_and_validate_date((today + timedelta(days=40)).strftime("%Y-%m-%d"))
    assert dt is None
    assert "30 ngày" in err

    dt, err = parse_and_validate_date("invalid-date")
    assert err == "Định dạng không hợp lệ (YYYY-MM-DD)"

def test_is_valid_working_day():
    doc = MagicMock()
    doc.profile.profile_type = "doctor"

    doc.profile.work_schedule = None
    assert is_valid_working_day(doc, date.today()) == (False, None)

    schedule = MagicMock()
    schedule.work_dates = [MagicMock(day_of_week=MagicMock(name="SUNDAY"))]
    schedule.work_dates[0].day_of_week.name = "SUNDAY"
    doc.profile.work_schedule = schedule

    target_date = datetime(2026, 4, 13)
    assert is_valid_working_day(doc, target_date)[0] is False

@patch('src.modules.doctors.services.get_upcoming_appointments', return_value=[])
def test_get_my_schedule_service(mock_get_appts):
    user = MagicMock()
    user.role.name = "PATIENT"
    res, code = get_my_schedule_service(user)
    assert code == "FORBIDDEN"

    user.role.name = "DOCTOR"
    user.profile.profile_type = "doctor"
    user.profile.work_schedule.title = "Lịch"
    user.profile.work_schedule.work_dates = [MagicMock()]
    user.profile.work_schedule.work_dates[0].day_of_week.name = "MONDAY"
    res, code = get_my_schedule_service(user)
    assert code == "SUCCESS"
    assert "workSchedule" in res

@patch('src.modules.doctors.services.is_conflict_appointment')
@patch('src.modules.doctors.services.get_or_create_work_schedule')
@patch('src.modules.doctors.services.update_work_dates')
@patch('src.modules.doctors.services.commit_session')
def test_request_schedule_change_service(m_commit, m_upd, m_get, m_conflict):
    user = MagicMock()
    user.role.name = "DOCTOR"
    user.profile.profile_type = "doctor"

    m_conflict.return_value = True
    res, code = request_schedule_change_service(user, {})
    assert code == "FORBIDDEN"

    m_conflict.return_value = False
    res, code = request_schedule_change_service(user, {})
    assert code == "ERROR_BAD_REQUEST"

    res, code = request_schedule_change_service(user, {"newWorkSchedule": {"start_time": "abc"}})
    assert code == "ERROR_BAD_REQUEST"

    payload = {
        "newWorkSchedule": {
            "start_time": "08:00:00", "end_time": "17:00:00", "work_date": ["MONDAY", "INVALID"]
        }
    }
    m_get.return_value = MagicMock()
    res, code = request_schedule_change_service(user, payload)
    assert code == "SUCCESS"

@patch('src.modules.doctors.services.get_specialty_by_id')
@patch('src.modules.doctors.services.get_medical_service_by_id')
def test_detail_services(mock_med, mock_spec):
    mock_spec.return_value = None
    res, code = get_specialty_detail_service(1)
    assert code == "NOT_FOUND"

    mock_med.return_value = None
    res, code = get_medical_service_detail_service(1)
    assert code == "NOT_FOUND"
