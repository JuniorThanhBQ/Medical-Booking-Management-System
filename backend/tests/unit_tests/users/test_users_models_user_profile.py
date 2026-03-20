import datetime

import pytest
from sqlalchemy.exc import IntegrityError
from src.modules.users.models import (GenderRole, PatientProfile, Profile,
                                      SlotStatus, User, UserRole)
from tests.unit_tests.test_base import test_app, test_session


@pytest.fixture
def valid_user_data():
    return {
        "username": "juniorthanh09",
        "password": "bam@&51722fasHASH",
        "first_name": "Thanh",
        "last_name": "Van",
        "email": "2351050164@ou.edu.vn",
        "role": UserRole.PATIENT,
        "is_active": True,
    }


@pytest.fixture
def valid_profile_data():
    return {
        "address": "97 Vo van tan",
        "phone": "0865726615",
        "gender": GenderRole.MALE,
        "avatar": "https://this_is_ou_edu_vn.com/image.png/",
    }


@pytest.fixture
def valid_specialty_data():
    return {
        "name": "Nha khoa",
        "description": "Chuyên các bệnh về răng miệng",
        "image": "https://this_is_ou_edu_vn.com/nhakhoa.png/",
    }


@pytest.fixture
def valid_work_schedule_data():
    return {"title": "Lịch làm việc", "description": "Sáng 8h-12h, Chiều 13h-17h"}


@pytest.fixture
def valid_time_slot_data():
    return {
        "start_time": datetime.time(8, 0),
        "end_time": datetime.time(9, 0),
        "date_slot": datetime.date(2023, 10, 1),
        "status": SlotStatus.AVAILABLE,
    }


def test_user_role_enum():
    assert UserRole.DOCTOR.value == 1
    assert UserRole.RECEPTIONIST.value == 2
    assert UserRole.PATIENT.value == 3
    assert UserRole.ADMIN.value == 4


def test_gender_role_enum():
    assert GenderRole.MALE.value == 1
    assert GenderRole.FEMALE.value == 2
    assert GenderRole.OTHER.value == 3
    assert GenderRole.NOT_SET.value == 4


def test_user_init(valid_user_data):
    user = User(**valid_user_data)
    assert user.username == "juniorthanh09"
    assert user.first_name == "Thanh"
    assert user.last_name == "Van"
    assert user.email == "2351050164@ou.edu.vn"
    assert user.role == UserRole.PATIENT
    assert user.is_active is True


def test_user_def_str(valid_user_data):
    user = User(**valid_user_data)
    assert str(user) == "juniorthanh09"


def test_edge_str_missing_username():
    user = User(first_name="Thanh")
    with pytest.raises(TypeError):
        str(user)


def test_user_create(test_session, valid_user_data):
    user = User(**valid_user_data)
    test_session.add(user)
    test_session.commit()
    created_user = test_session.query(User).filter_by(username="juniorthanh09").first()
    assert created_user is not None
    assert created_user.email == "2351050164@ou.edu.vn"


def test_create_duplicate_username(test_session, valid_user_data):
    user1 = User(**valid_user_data)
    test_session.add(user1)
    test_session.commit()
    user2 = User(**valid_user_data)
    test_session.add(user2)
    with pytest.raises(IntegrityError):
        test_session.commit()


def test_user_update(test_session, valid_user_data):
    user = User(**valid_user_data)
    test_session.add(user)
    test_session.commit()
    user.first_name = "Thanh"
    test_session.commit()
    updated_user = test_session.query(User).filter_by(username="juniorthanh09").first()
    assert updated_user.first_name == "Thanh"


def test_user_delete(test_session, valid_user_data):
    user = User(**valid_user_data)
    test_session.add(user)
    test_session.commit()
    test_session.delete(user)
    test_session.commit()
    deleted_user = test_session.query(User).filter_by(username="juniorthanh09").first()
    assert deleted_user is None


def test_profile_init(valid_profile_data):
    profile_data = {**valid_profile_data, "user_id": 1}
    profile = Profile(**profile_data)
    assert profile.address == "97 Vo van tan"
    assert profile.phone == "0865726615"
    assert profile.gender == GenderRole.MALE
    assert profile.avatar == "https://this_is_ou_edu_vn.com/image.png/"
    assert profile.user_id == 1


def test_profile_def_str(valid_profile_data):
    user = User(first_name="Trung Thanh", last_name="Van")
    profile = Profile(**valid_profile_data, user_id=1)
    profile.user = user
    assert str(profile) == "Van Trung Thanh"


def test_edge_str_missing_user(valid_profile_data):
    profile = Profile(**valid_profile_data, user_id=1)
    with pytest.raises(AttributeError):
        str(profile)


def test_profile_relationship(test_session, valid_user_data, valid_profile_data):
    user = User(**valid_user_data)
    test_session.add(user)
    test_session.commit()
    profile = Profile(**valid_profile_data, user_id=user.id)
    test_session.add(profile)
    test_session.commit()
    created_profile = test_session.query(Profile).filter_by(user_id=user.id).first()
    assert created_profile.user.first_name == "Thanh"
    assert created_profile.user.email == "2351050164@ou.edu.vn"


def test_patient_profile_init(valid_profile_data):
    patient_data = {
        **valid_profile_data,
        "user_id": 1,
        "medical_history": "Bệnh tim nhẹ",
    }
    patient = PatientProfile(**patient_data)
    assert patient.medical_history == "Bệnh tim nhẹ"
    assert patient.gender == GenderRole.MALE


def test_patient_profile_create(test_session, valid_user_data, valid_profile_data):
    user = User(**valid_user_data)
    test_session.add(user)
    test_session.commit()
    patient_data = {
        **valid_profile_data,
        "user_id": user.id,
        "medical_history": "Bệnh tim nhẹ",
    }
    patient = PatientProfile(**patient_data)
    test_session.add(patient)
    test_session.commit()
    saved_patient = (
        test_session.query(PatientProfile).filter_by(user_id=user.id).first()
    )
    assert saved_patient is not None
    assert saved_patient.medical_history == "Bệnh tim nhẹ"


def test_patient_profile_def_str(valid_profile_data):
    user = User(first_name="Trung Thành", last_name="Văn")
    patient = PatientProfile(**valid_profile_data, user_id=1)
    patient.user = user
    assert str(patient) == "Văn Trung Thành"
