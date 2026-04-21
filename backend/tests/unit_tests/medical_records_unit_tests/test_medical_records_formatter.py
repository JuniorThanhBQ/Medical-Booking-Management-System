from types import SimpleNamespace
from datetime import datetime

from src.utils.medical_records.formatter_utils import format_medical_record


def make_record():
    now = datetime(2026, 4, 1, 10, 0)
    patient_user = SimpleNamespace(first_name='An', last_name='Nguyen')
    doctor_user = SimpleNamespace(first_name='Dr', last_name='Who')
    specialty = SimpleNamespace(name='Tim mạch')
    ms = SimpleNamespace(name='Service')
    status = SimpleNamespace(name='COMPLETED')
    appointment = SimpleNamespace(id=2, medical_service=ms, status=status)
    doctor = SimpleNamespace(user=doctor_user, specialty=specialty)
    patient = SimpleNamespace(user=patient_user)
    return SimpleNamespace(id=123, appointment=appointment, doctor=doctor, patient=patient, diagnosis='dx', created_date=now)


def test_format_medical_record():
    r = make_record()
    out = format_medical_record(r)
    assert out['id'] == str(123)
    assert out['patientName'].startswith('Nguyen')
    assert out['doctorName'].startswith('Who')
    assert out['service'] == 'Service'
