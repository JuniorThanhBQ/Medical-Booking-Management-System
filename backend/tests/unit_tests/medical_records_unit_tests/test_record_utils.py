from types import SimpleNamespace

from src.utils.medical_records.record_utils import \
    check_record_access_permission


def make_user(role_name, profile_id=None):
    role = SimpleNamespace(name=role_name)
    profile = SimpleNamespace(id=profile_id) if profile_id is not None else None
    return SimpleNamespace(role=role, profile=profile)


def make_record(patient_profile_id=None, doctor_profile_id=None):
    return SimpleNamespace(patient_profile_id=patient_profile_id, doctor_profile_id=doctor_profile_id)


def test_patient_access_allowed():
    user = make_user('PATIENT', profile_id=5)
    record = make_record(patient_profile_id=5)
    assert check_record_access_permission(user, record) is True


def test_patient_access_denied():
    user = make_user('PATIENT', profile_id=5)
    record = make_record(patient_profile_id=6)
    assert check_record_access_permission(user, record) is False


def test_doctor_access_allowed():
    user = make_user('DOCTOR', profile_id=2)
    record = make_record(doctor_profile_id=2)
    assert check_record_access_permission(user, record) is True


def test_doctor_access_denied():
    user = make_user('DOCTOR', profile_id=2)
    record = make_record(doctor_profile_id=3)
    assert check_record_access_permission(user, record) is False


def test_other_role_allowed():
    user = make_user('ADMIN', profile_id=None)
    record = make_record(patient_profile_id=1, doctor_profile_id=2)
    assert check_record_access_permission(user, record) is True
