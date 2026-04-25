from datetime import datetime

from src.utils.appointment.formatter_utils import (
    parse_appointment_datetime,
    format_appointment,
)

def make_appointment(dt=None):
    now = dt or datetime(2026, 4, 1, 9, 30, 0)
    ms = {'name': 'Khám tổng quát'}
    status = {'name': 'PENDING'}
    return {
        'id': 1,
        'medical_service': ms,
        'name': 'Checkup',
        'patient_profile': {'first_name': 'An', 'last_name': 'Nguyễn'},
        'appointment_date': now,
        'status': status,
        'note': 'note',
        'created_date': now,
        'updated_date': now,
    }


def test_parse_appointment_datetime_valid():
    s = '2026-04-01T09:30:00.000+07:00'
    dt, err = parse_appointment_datetime(s)

    assert err is None
    assert isinstance(dt, datetime)


def test_parse_appointment_datetime_invalid():
    dt, err = parse_appointment_datetime('bad-format')

    assert dt is None
    assert err[1] == 'ERROR_BAD_REQUEST'


def test_format_appointment_defaults():
    appt = make_appointment()
    doctor = {'first_name': 'B', 'last_name': 'C'}
    out = format_appointment(appointment=appt, doctor=doctor)

    assert out['id'] == 1
    assert out['service'] == 'Khám tổng quát'
    assert out['patientName'] == 'Nguyễn An'
    assert out['doctorName'] == 'C B'
    assert out['appointmentDate'].endswith('+07:00')
