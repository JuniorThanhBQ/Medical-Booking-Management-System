from datetime import datetime, time, timedelta

from src.extensions import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.doctors.models import (DayOfWeek, DoctorProfile,
                                        MedicalService, Specialty, WorkDate,
                                        WorkSchedule)
from src.modules.doctors.repositories import (commit_session, get_doctor_by_id,
                                              get_medical_service_by_id,
                                              get_or_create_work_schedule,
                                              get_paginated_doctors,
                                              get_paginated_medical_services,
                                              get_paginated_specialties,
                                              get_specialty_by_id,
                                              get_upcoming_appointments,
                                              is_conflict_appointment,
                                              update_work_dates)
from src.modules.users.models import User, UserRole
from tests.test_base import test_app, test_client, test_session


def test_doctors_repositories(test_app, test_session):
    with test_app.app_context():
        spec = Specialty(name="Tim mạch", description="Khoa tim", level="Chuyên khoa")
        db.session.add(spec)
        db.session.commit()

        med_srv = MedicalService(name="Siêu âm tim", specialty_id=spec.id)
        db.session.add(med_srv)
        db.session.commit()

        user = User(username="dr_tim", email="tim@test.com", password="123",
                    first_name="A", last_name="B", role=UserRole.DOCTOR, is_active=True)
        db.session.add(user)
        db.session.commit()

        if user.profile:
            db.session.delete(user.profile)
            db.session.commit()

        dp = DoctorProfile(
            user_id=user.id,
            specialty_id=spec.id,
            title="BS",
            bio="Bio"
        )
        db.session.add(dp)
        db.session.commit()

        ws = WorkSchedule(
            doctor_id=dp.id,
            title="Lịch Hè",
            start_time=time(8, 0, 0),
            end_time=time(13, 0, 0)
        )
        db.session.add(ws)
        db.session.commit()

        wd = WorkDate(day_of_week=DayOfWeek.MONDAY, work_schedule_id=ws.id)
        db.session.add(wd)
        db.session.commit()

        now = datetime.now()
        apt = Appointment( name="Testappointment", note="Appointment", medical_service_id=1,
            doctor_profile_id=dp.id, patient_profile_id=1,
            appointment_date=now + timedelta(days=1), status=StatusRole.APPROVED
        )
        db.session.add(apt)
        db.session.commit()

        assert get_specialty_by_id(spec.id).name == "Tim mạch"
        paginated_spec = get_paginated_specialties(1, 10, keywords="tim")
        assert len(paginated_spec.items) == 1

        assert get_medical_service_by_id(med_srv.id).name == "Siêu âm tim"
        paginated_med = get_paginated_medical_services(1, 10, keywords="siêu âm", specialty_id=spec.id)
        assert len(paginated_med.items) == 1

        assert get_doctor_by_id(dp.id).email == "tim@test.com"

        paginated_docs = get_paginated_doctors(1, 10, keywords="A", specialty_id=spec.id, work_days=[DayOfWeek.MONDAY])
        assert len(paginated_docs.items) == 1

        upcoming = get_upcoming_appointments(dp.id, now, [StatusRole.APPROVED])
        assert len(upcoming) == 1

        conflict = is_conflict_appointment(dp.id, now, now + timedelta(days=2), [StatusRole.APPROVED])
        assert conflict is not None

        existing_ws = get_or_create_work_schedule(dp.id)
        assert existing_ws.id == ws.id

        new_ws = get_or_create_work_schedule(999)
        assert new_ws.doctor_id == 999

        update_work_dates(ws.id, [DayOfWeek.TUESDAY])
        updated_wds = WorkDate.query.filter_by(work_schedule_id=ws.id).all()
        assert len(updated_wds) == 1
        assert updated_wds[0].day_of_week == DayOfWeek.TUESDAY

        commit_session()