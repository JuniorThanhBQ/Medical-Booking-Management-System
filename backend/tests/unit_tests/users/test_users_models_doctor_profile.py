import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from src.modules.users.models import (DoctorProfile, SlotStatus, Specialty,
                                      TimeSlot, User, WorkSchedule)
from tests.unit_tests.test_base import test_app, test_session
from tests.unit_tests.users.test_users_models_user_profile import (
    valid_profile_data, valid_specialty_data, valid_time_slot_data,
    valid_user_data, valid_work_schedule_data)


def test_doctor_profile_init(valid_profile_data):
    doctor_data = {
        **valid_profile_data,
        "user_id": 1,
        "about": "Bác sĩ chuyên khoa 10 năm kinh nghiệm",
        "year_of_experience": 10,
        "specialty_id": 1,
        "work_schedule_id": 1,
    }
    doctor = DoctorProfile(**doctor_data)

    assert doctor.about == "Bác sĩ chuyên khoa 10 năm kinh nghiệm"
    assert doctor.year_of_experience == 10
    assert doctor.specialty_id == 1
    assert doctor.work_schedule_id == 1
    assert doctor.address == "97 Vo van tan"


def test_doctor_profile_create(
    test_session,
    valid_user_data,
    valid_profile_data,
    valid_specialty_data,
    valid_work_schedule_data,
):
    user = User(**valid_user_data)
    test_session.add(user)
    test_session.commit()

    specialty = Specialty(**valid_specialty_data)
    test_session.add(specialty)
    test_session.commit()

    ws = WorkSchedule(**valid_work_schedule_data)
    test_session.add(ws)
    test_session.commit()

    doctor_data = {
        **valid_profile_data,
        "user_id": user.id,
        "about": "Bác sĩ chuyên khoa 10 năm kinh nghiệm",
        "year_of_experience": 10,
        "specialty_id": specialty.id,
        "work_schedule_id": ws.id,
    }
    doctor = DoctorProfile(**doctor_data)
    test_session.add(doctor)
    test_session.commit()

    saved_doctor = test_session.query(DoctorProfile).filter_by(user_id=user.id).first()

    assert saved_doctor is not None
    assert saved_doctor.year_of_experience == 10
    assert saved_doctor.specialty.name == "Nha khoa"
    assert saved_doctor.work_schedule.title == "Lịch làm việc"


def test_doctor_profile_missing_required_fields(
    test_session, valid_user_data, valid_profile_data
):
    user = User(**valid_user_data)
    test_session.add(user)
    test_session.commit()
    doctor_data = {
        **valid_profile_data,
        "user_id": 1,
        "about": "Bác sĩ chuyên khoa 10 năm kinh nghiệm",
    }
    doctor = DoctorProfile(**doctor_data)
    test_session.add(doctor)
    with pytest.raises(IntegrityError):
        test_session.commit()


def test_slot_status_enum():
    assert SlotStatus.LOCKER.value == 1
    assert SlotStatus.OCCUPIED.value == 2
    assert SlotStatus.AVAILABLE.value == 3


def test_specialty_init(valid_specialty_data):
    specialty = Specialty(**valid_specialty_data)
    assert specialty.name == "Nha khoa"
    assert specialty.description == "Chuyên các bệnh về răng miệng"
    assert specialty.image == "https://this_is_ou_edu_vn.com/nhakhoa.png/"


def test_specialty_def_str(valid_specialty_data):
    specialty = Specialty(**valid_specialty_data)
    assert str(specialty) == "Nha khoa"


def test_specialty_create(test_session, valid_specialty_data):
    specialty = Specialty(**valid_specialty_data)
    test_session.add(specialty)
    test_session.commit()
    saved_specialty = test_session.query(Specialty).filter_by(name="Nha khoa").first()
    assert saved_specialty is not None


def test_create_duplicate_specialty_name(test_session, valid_specialty_data):
    spec1 = Specialty(**valid_specialty_data)
    test_session.add(spec1)
    test_session.commit()
    spec2 = Specialty(**valid_specialty_data)
    test_session.add(spec2)
    with pytest.raises(IntegrityError):
        test_session.commit()


def test_work_schedule_init(valid_work_schedule_data):
    ws = WorkSchedule(**valid_work_schedule_data)
    assert ws.title == "Lịch làm việc"
    assert ws.description == "Sáng 8h-12h, Chiều 13h-17h"


def test_work_schedule_def_str(valid_work_schedule_data):
    ws = WorkSchedule(**valid_work_schedule_data)
    assert str(ws) == "Lịch làm việc"


def test_work_schedule_create(test_session, valid_work_schedule_data):
    ws = WorkSchedule(**valid_work_schedule_data)
    test_session.add(ws)
    test_session.commit()
    saved_ws = test_session.query(WorkSchedule).filter_by(title="Lịch làm việc").first()
    assert saved_ws is not None


def test_time_slot_init(valid_time_slot_data):
    ts_data = {**valid_time_slot_data, "work_schedule_id": 1}
    ts = TimeSlot(**ts_data)
    assert ts.start_time == datetime.time(8, 0)
    assert ts.end_time == datetime.time(9, 0)
    assert ts.date_slot == datetime.date(2023, 10, 1)
    assert ts.status == SlotStatus.AVAILABLE
    assert ts.work_schedule_id == 1


def test_time_slot_def_str(valid_time_slot_data, valid_work_schedule_data):
    ws = WorkSchedule(**valid_work_schedule_data)
    ts = TimeSlot(**valid_time_slot_data, work_schedule_id=1)
    ts.work_schedule = ws
    assert str(ts) == "Lịch làm việc - 2023-10-01"


def test_time_slot_create_relationship(
    test_session, valid_work_schedule_data, valid_time_slot_data
):
    ws = WorkSchedule(**valid_work_schedule_data)
    test_session.add(ws)
    test_session.commit()
    ts_data = {**valid_time_slot_data, "work_schedule_id": ws.id}
    ts = TimeSlot(**ts_data)
    test_session.add(ts)
    test_session.commit()
    saved_ts = test_session.query(TimeSlot).filter_by(work_schedule_id=ws.id).first()
    assert saved_ts is not None
    assert saved_ts.work_schedule.title == "Lịch làm việc"


def test_edge_time_slot_str_missing(valid_time_slot_data):
    ts = TimeSlot(**valid_time_slot_data, work_schedule_id=1)
    with pytest.raises(AttributeError):
        str(ts)
