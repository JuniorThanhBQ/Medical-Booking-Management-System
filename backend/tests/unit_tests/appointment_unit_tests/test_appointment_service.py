from datetime import datetime, date, timedelta, timezone

import pytest

from src.modules.appointments.services import (
    AppointmentService,
    handle_status_update,
)
from src.modules.appointments.models import StatusRole


def test_handle_status_update():
    appt = {'status': StatusRole.PENDING}
    assert handle_status_update(appt, 'COMPLETED') is None
    assert appt["status"] == StatusRole.COMPLETED

    err = handle_status_update(appt, 'NON_EXISTENT')
    assert isinstance(err, tuple)


def make_service_with_mocks():
    class MockRepo:
        def __init__(self):
            self._locks = []

        def __getitem__(self, key):
            return getattr(self, key)

        def __setitem__(self, key, value):
            setattr(self, key, value)

        def update(self, data):
            self.__dict__.update(data)

    repo = MockRepo()

    repo.add_instance = lambda x: repo.update({'last_added': x})
    repo.commit_session = lambda: repo.update({'committed': True})
    repo.get_patient_profile_by_details = lambda *a, **k: None
    repo.create_new_patient_profile = lambda *a, **k: {'id': 99, 'phone': a[2]}
    repo.get_appointment_by_id = lambda _id: None

    def clean_expired_booking_locks(minutes=20):
        now = datetime.now(timezone.utc)
        repo._locks = [
            l for l in repo._locks
            if (now - l["created_date"]).total_seconds() < minutes * 60
        ]

    def get_active_booking_lock(doctor_name, appointment_date):
        for l in repo._locks:
            if (
                l["doctor_name"] == doctor_name
                and l["appointment_date"].replace(microsecond=0)
                == appointment_date.replace(microsecond=0)
            ):
                return l
        return None

    def create_booking_lock(doctor_name, appointment_date, service_name):
        lock = {
            'doctor_name': doctor_name,
            'appointment_date': appointment_date,
            'service_name': service_name,
            'created_date': datetime.now(timezone.utc)
        }
        repo._locks.append(lock)
        return lock

    def delete_booking_lock(doctor_name, appointment_date):
        repo._locks = [
            l for l in repo._locks
            if not (
                l["doctor_name"] == doctor_name
                and l["appointment_date"].replace(microsecond=0)
                == appointment_date.replace(microsecond=0)
            )
        ]

    repo.clean_expired_booking_locks = clean_expired_booking_locks
    repo.get_active_booking_lock = get_active_booking_lock
    repo.create_booking_lock = create_booking_lock
    repo.delete_booking_lock = delete_booking_lock

    doctor_repo = {}
    doctor_service = {}

    svc = AppointmentService(repo, doctor_repo, doctor_service)
    return svc, repo, doctor_repo, doctor_service


def test_validate_appointment_booking_success():
    svc, repo, doctor_repo, doctor_service = make_service_with_mocks()

    doctor = {
        "profile": {"specialty_id": 1, "id": 5},
        "user": {"first_name": "A", "last_name": "B"},
        "role": {"name": "DOCTOR"},
        "is_active": True
    }

    medical_service = {
        "id": 2,
        "specialty_id": 1
    }

    doctor_repo["get_doctor_by_id"] = lambda _id: doctor
    doctor_repo["get_medical_service_by_id"] = lambda sid: medical_service

    target_dt = datetime.now(timezone.utc) + timedelta(days=2)
    appt_str = target_dt.strftime('%Y-%m-%dT%H:%M:%S.000+07:00')
    slot_str = target_dt.strftime('%Y-%m-%dT%H:%M:%S+07:00')

    doctor_service["get_available_time_slots"] = lambda d, td, ms: [slot_str]

    dt, d, ms, err = svc.validate_appointment_booking(1, appt_str, 2)

    assert err is None
    assert isinstance(dt, datetime)
    assert d == doctor


def test_get_or_create_patient_profile_existing_and_new():
    svc, repo, _, _ = make_service_with_mocks()

    existing = {'id': 5}
    repo["get_patient_profile_by_details"] = lambda *a, **k: existing

    p, e = svc.get_or_create_patient_profile({
        'firstName': 'F', 'lastName': 'L', 'phone': '012',
        'gender': 'MALE', 'birthday': '1990-01-01', 'address': 'A'
    })
    assert p is existing

    repo["get_patient_profile_by_details"] = lambda *a, **k: None
    repo["create_new_patient_profile"] = lambda *a, **k: {'id': 7, 'phone': a[2]}

    p2, e2 = svc.get_or_create_patient_profile({
        'firstName': 'F', 'lastName': 'L', 'phone': '012',
        'gender': 'MALE', 'birthday': '1990-01-01', 'address': 'A'
    })
    assert p2["id"] == 7


def test_validate_appointment_request_forbidden_and_missing():
    svc, repo, _, _ = make_service_with_mocks()

    user = {"role": {"name": "DOCTOR"}}
    appt_date, d, ms, err = svc.validate_appointment_request(user, {})
    assert err is not None

    user2 = {"role": {"name": "PATIENT"}}
    appt_date, d, ms, err2 = svc.validate_appointment_request(user2, {'doctorId': None})
    assert err2 is not None

def test_handle_date_update_changes_date_and_validates():
    svc, repo, doctor_repo, doctor_service = make_service_with_mocks()

    base = datetime.now(timezone.utc) + timedelta(days=1)

    appt = {
        "appointment_date": base,
        "doctor": {"user": {}},
        "medical_service": {"id": 1}
    }

    new_dt = base + timedelta(days=1)
    new_date_str = new_dt.strftime('%Y-%m-%dT%H:%M:%S.000+07:00')

    doctor_service["get_available_time_slots"] = lambda user, td, ms: [
        new_dt.strftime('%Y-%m-%dT%H:%M:%S+07:00')
    ]

    res = svc.handle_date_update(appt, new_date_str)
    assert res is None
    assert appt["appointment_date"].date() == new_dt.date()

    bad = svc.handle_date_update(appt, 'bad-date')
    assert bad is not None


def test_lock_and_unlock_booking_transaction_service():
    svc, repo, _, _ = make_service_with_mocks()
    target = datetime.now(timezone.utc) + timedelta(days=3)
    data = {'doctorName': 'drx', 'appointmentDate': target.strftime('%Y-%m-%dT%H:%M:%S.000+07:00'), 'serviceName': 'S'}
    ok, code = svc.lock_booking_transaction_service(data)
    assert code == 'SUCCESS'

    ok2, code2 = svc.lock_booking_transaction_service(data)
    assert code2 in ('CONFLICT', 'SUCCESS')

    uok, ucode = svc.unlock_booking_transaction_service({'doctorName': 'drx', 'appointmentDate': data['appointmentDate']})
    assert ucode == 'SUCCESS'
