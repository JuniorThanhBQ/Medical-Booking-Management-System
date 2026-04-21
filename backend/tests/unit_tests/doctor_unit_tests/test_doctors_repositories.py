from datetime import datetime, time, date, timedelta, timezone
from types import SimpleNamespace

from tests.test_base import create_app
from src.extensions import db

from src.modules.doctors.repositories import DoctorRepository
from src.modules.doctors.models import Specialty, MedicalService, VisitType, WorkSchedule, WorkDate, DayOfWeek, DoctorProfile
from src.modules.users.models import User, UserRole


def create_specialty(session, name='Spec'):
    s = Specialty(name=name, description='d', level='Cơ sở')
    session.add(s)
    session.flush()
    return s


def create_user_and_doctor(session, specialty_id):
    u = User(username='d1', password='p', email='d1@x', first_name='A', last_name='B', role=UserRole.DOCTOR, is_active=True)
    session.add(u)
    session.flush()
    dp = DoctorProfile(user_id=u.id, title='T', bio='bio', specialty_id=specialty_id)
    session.add(dp)
    session.flush()
    return u, dp


def setup_db():
    app = create_app()
    app.config['DISABLE_SIGNALS'] = True
    ctx = app.app_context()
    ctx.push()
    db.create_all()
    return ctx


def teardown_db(ctx):
    db.session.remove()
    db.drop_all()
    try:
        db.engine.dispose()
    except Exception:
        pass
    ctx.pop()


def test_specialty_and_service_pagination():
    ctx = setup_db()
    try:
        repo = DoctorRepository()
        s1 = create_specialty(db.session, 'Cardio')
        s2 = create_specialty(db.session, 'Skin')

        ms1 = MedicalService(name='Service A', description='d', specialty_id=s1.id)
        ms2 = MedicalService(name='Service B', description='d', specialty_id=s1.id)
        db.session.add_all([ms1, ms2])
        db.session.flush()

        page = repo.get_paginated_specialties(page=1, per_page=10, keywords='Card')
        assert page.items

        mpage = repo.get_paginated_medical_services(page=1, per_page=10, specialty_id=s1.id)
        assert any(ms.name == 'Service A' for ms in mpage.items)
    finally:
        teardown_db(ctx)


def test_get_doctor_ids_by_work_day_and_paginated_doctors():
    ctx = setup_db()
    try:
        repo = DoctorRepository()
        spec = create_specialty(db.session, 'X')
        u, dp = create_user_and_doctor(db.session, spec.id)

        ws = WorkSchedule(title='W', description='d', start_time=time(8,0), end_time=time(12,0), doctor_id=dp.id)
        db.session.add(ws)
        db.session.flush()
        wd = WorkDate(day_of_week=DayOfWeek.MONDAY, work_schedule_id=ws.id)
        db.session.add(wd)
        db.session.flush()

        ids = repo.get_doctor_ids_by_work_day('monday')
        assert dp.id in ids

        paged = repo.get_paginated_doctors(page=1, per_page=10, work_days='monday')
        assert paged.items
    finally:
        teardown_db(ctx)


def test_get_doctor_by_id_and_work_schedule_creation():
    ctx = setup_db()
    try:
        repo = DoctorRepository()
        spec = create_specialty(db.session, 'Y')
        u, dp = create_user_and_doctor(db.session, spec.id)

        fetched = repo.get_doctor_by_id(dp.id)
        assert fetched is not None

        db.session.query(WorkSchedule).filter_by(doctor_id=dp.id).delete()
        db.session.flush()
        ws = repo.get_or_create_work_schedule(dp.id)
        assert ws is not None
    finally:
        teardown_db(ctx)


def test_booked_and_upcoming_appointments_and_conflict():
    from src.modules.appointments.models import Appointment, StatusRole

    ctx = setup_db()
    try:
        repo = DoctorRepository()
        spec = create_specialty(db.session, 'Z')
        u, dp = create_user_and_doctor(db.session, spec.id)

        base = datetime.now(timezone.utc)
        appt1 = Appointment(name='a1', note='n', appointment_date=base + timedelta(days=1, hours=9), doctor_profile_id=dp.id, patient_profile_id=dp.id, medical_service_id=1, status=StatusRole.APPROVED)
        appt2 = Appointment(name='a2', note='n', appointment_date=base + timedelta(days=2, hours=10), doctor_profile_id=dp.id, patient_profile_id=dp.id, medical_service_id=1, status=StatusRole.PENDING)
        db.session.add_all([appt1, appt2])
        db.session.flush()

        booked = repo.get_booked_appointments(dp.id, (base + timedelta(days=1)).date())
        assert any(a.name == 'a1' for a in booked)

        upcoming = repo.get_upcoming_appointments(dp.id, base, [StatusRole.APPROVED, StatusRole.PENDING])
        assert len(upcoming) >= 2

        conflict = repo.is_conflict_appointment(dp.id, base + timedelta(days=1, hours=8), base + timedelta(days=1, hours=10), [StatusRole.APPROVED])
        assert conflict is not None
    finally:
        teardown_db(ctx)
