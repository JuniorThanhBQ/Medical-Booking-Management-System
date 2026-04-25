from tests.test_base import test_app
from src.utils.medical_records.formatter_utils import format_medical_record

from types import SimpleNamespace
from datetime import datetime

def make_record():
    now = datetime(2026, 4, 1, 10, 0)

    return SimpleNamespace(
        id=123,
        diagnosis="dx",
        created_date=now,

        appointment=SimpleNamespace(
            id=2,
            medical_service=SimpleNamespace(name="Service"),
            status=SimpleNamespace(name="COMPLETED")
        ),

        doctor=SimpleNamespace(
            user=SimpleNamespace(first_name="Dr", last_name="Who"),
            specialty=SimpleNamespace(name="Tim mạch")
        ),

        patient=SimpleNamespace(
            user=SimpleNamespace(first_name="An", last_name="Nguyen")
        )
    )

def test_format_medical_record():
    r = make_record()
    out = format_medical_record(r)

    assert out['id'] == str(123)
    assert out['patientName'].startswith('Nguyen')
    assert out['doctorName'].startswith('Who')
    assert out['service'] == 'Service'
