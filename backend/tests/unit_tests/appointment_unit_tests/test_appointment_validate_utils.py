from datetime import datetime, date, timedelta
from tests.test_base import test_app
from src.utils.appointment.appointment_validate_utils import (
    validate_appointment_date,
    validate_available_slot,
    validate_doctor,
)


def test_validate_appointment_date_within_range():
    dt = datetime.now() + timedelta(days=1)
    err, code = validate_appointment_date(dt)

    assert err is None and code is None


def test_validate_appointment_date_out_of_range():
    dt = datetime.now() + timedelta(days=31)
    err, code = validate_appointment_date(dt)

    assert err is not None


def test_validate_available_slot_ok():
    dt = datetime(2026, 4, 1, 9, 0, 0)
    slots = [dt.isoformat() + '+07:00']
    err, code = validate_available_slot(dt, slots)

    assert err is None


def test_validate_available_slot_not_ok():
    dt = datetime(2026, 4, 1, 10, 0, 0)
    slots = ['2026-04-01T09:00:00+07:00']
    err, code = validate_available_slot(dt, slots)

    assert err is not None


def test_validate_doctor_ok():
    doc = {'role': {'name': 'DOCTOR'}, 'is_active': True}
    err, code = validate_doctor(doc)

    assert err is None


def test_validate_doctor_invalid():
    doc = {'role': {'name': 'RECEPTIONIST'}, 'is_active': True}
    err, code = validate_doctor(doc)

    assert err is not None
