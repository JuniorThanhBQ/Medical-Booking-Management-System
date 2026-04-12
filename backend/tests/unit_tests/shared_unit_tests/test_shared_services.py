from datetime import date, datetime, timedelta
from unittest.mock import MagicMock

import pytest

from src.modules.shared.services import (check_is_conflicting,
                                         format_appointment,
                                         format_speciality_output,
                                         parse_appointment_datetime,
                                         validate_appointment_date,
                                         validate_available_slot)


def test_parse_appointment_datetime():
    dt, err = parse_appointment_datetime("2026-04-12T10:30:00Z")
    assert dt == datetime(2026, 4, 12, 10, 30, 0)
    assert err is None

    dt, err = parse_appointment_datetime("2026-04-12T10:30:00.123Z")
    assert dt == datetime(2026, 4, 12, 10, 30, 0)
    assert err is None

    dt, err = parse_appointment_datetime("ngay-khong-hop-le")
    assert dt is None
    assert err[0]["message"] == "Định dạng ngày không hợp lệ"
    assert err[1] == "ERROR_BAD_REQUEST"

def test_validate_appointment_date():
    today = date.today()

    valid_dt = datetime.combine(today + timedelta(days=3), datetime.min.time())
    err, code = validate_appointment_date(valid_dt)
    assert err is None
    assert code is None

    past_dt = datetime.combine(today - timedelta(days=1), datetime.min.time())
    err, code = validate_appointment_date(past_dt)
    assert code == "ERROR_BAD_REQUEST"
    assert "7 ngày tới" in err["message"]

    future_dt = datetime.combine(today + timedelta(days=8), datetime.min.time())
    err, code = validate_appointment_date(future_dt)
    assert code == "ERROR_BAD_REQUEST"

def test_validate_available_slot():
    dt = datetime(2026, 4, 12, 10, 30, 0)
    available_slots = ["2026-04-12T10:00:00Z", "2026-04-12T10:30:00Z"]

    err, code = validate_available_slot(dt, available_slots)
    assert err is None

    dt_invalid = datetime(2026, 4, 12, 11, 00, 0)
    err, code = validate_available_slot(dt_invalid, available_slots)
    assert code == "ERROR_BAD_REQUEST"
    assert err["message"] == "Khung giờ không khả dụng"

def test_format_appointment():
    mock_apt = MagicMock()
    mock_apt.id = 1
    mock_apt.name = "Khám tổng quát"
    mock_apt.appointment_date = datetime(2026, 4, 12, 10, 0)
    mock_apt.created_date = datetime(2026, 4, 1, 10, 0)
    mock_apt.updated_date = datetime(2026, 4, 2, 10, 0)
    mock_apt.note = "Không"

    mock_apt.medical_service.name = "Dịch vụ Nội khoa"
    mock_apt.status.name = "APPROVED"

    mock_doc = MagicMock()
    mock_doc.last_name = "Nguyen"
    mock_doc.first_name = "Bac Si"

    mock_patient = MagicMock()
    mock_patient.last_name = "Tran"
    mock_patient.first_name = "Benh Nhan"

    res = format_appointment(mock_apt, mock_doc, patient_name="Ten Truyen Vao")
    assert res["patientName"] == "Ten Truyen Vao"
    assert res["doctorName"] == "Nguyen Bac Si"
    assert res["service"] == "Dịch vụ Nội khoa"

    res2 = format_appointment(mock_apt, mock_doc, patient_user=mock_patient)
    assert res2["patientName"] == "Tran Benh Nhan"

    mock_apt.medical_service = None
    mock_apt.status = None
    res3 = format_appointment(mock_apt, doctor=None, patient_user=mock_patient)
    assert res3["doctorName"] is None
    assert res3["service"] is None
    assert res3["status"] is None

def test_check_is_conflicting():
    slot_start = datetime(2026, 4, 12, 10, 0)

    apt_no_conflict = MagicMock()
    apt_no_conflict.appointment_date = datetime(2026, 4, 12, 10, 30)
    apt_no_conflict.medical_service.visit_type.duration_minutes = 30
    apt_no_conflict.medical_service.visit_type.buffer_before = 0
    apt_no_conflict.medical_service.visit_type.buffer_after = 0

    apt_conflict = MagicMock()
    apt_conflict.appointment_date = datetime(2026, 4, 12, 9, 45)
    apt_conflict.medical_service = None

    is_conflict = check_is_conflicting(slot_start, 30, [apt_no_conflict])
    assert is_conflict is False

    is_conflict2 = check_is_conflicting(slot_start, timedelta(minutes=30), [apt_conflict])
    assert is_conflict2 is True

def test_format_speciality_output():
    mock_spec = MagicMock()
    mock_spec.id = 99
    mock_spec.name = "Nhi khoa"
    mock_spec.description = "Mô tả nhi khoa"
    mock_spec.level = 1

    res = format_speciality_output(mock_spec)

    assert res == {
        "id": 99,
        "name": "Nhi khoa",
        "description": "Mô tả nhi khoa",
        "level": 1
    }