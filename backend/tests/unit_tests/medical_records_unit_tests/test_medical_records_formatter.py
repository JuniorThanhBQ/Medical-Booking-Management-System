from tests.test_base import test_app
from src.utils.medical_records.formatter_utils import format_medical_record

from datetime import datetime

def make_record():
    now = datetime(2026, 4, 1, 10, 0)

    return {
        "id": 123,
        "diagnosis": "dx",
        "created_date": now,

        "appointment": {
            "id": 2,
            "medical_service": {"name": "Service"},
            "status": {"name": "COMPLETED"}
        },

        "doctor": {
            "user": {"first_name": "Dr", "last_name": "Who"},
            "specialty": {"name": "Tim mạch"}
        },

        "patient": {
            "user": {"first_name": "An", "last_name": "Nguyen"}
        }
    }

def test_format_medical_record():
    r = make_record()
    out = format_medical_record(r)

    assert out['id'] == str(123)
    assert out['patientName'].startswith('Nguyen')
    assert out['doctorName'].startswith('Who')
    assert out['service'] == 'Service'
