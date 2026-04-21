from datetime import datetime, timedelta, date, timezone
from tests.test_base import create_app
from src.extensions import db

from src.modules.appointments.repositories import AppointmentRepository
from src.modules.users.models import GenderRole


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


def test_create_and_get_patient_profile():
    ctx = setup_db()
    try:
        repo = AppointmentRepository()
        birthday = date.today()
        profile = repo.create_new_patient_profile('First', 'Last', '012345', GenderRole.MALE, birthday, 'Addr')
        db.session.flush()

        found = repo.get_patient_profile_by_details('First', 'Last', '012345', GenderRole.MALE, birthday, 'Addr')
        assert found is not None
        assert found.phone == '012345'
    finally:
        teardown_db(ctx)


def test_booking_lock_lifecycle():
    ctx = setup_db()
    try:
        repo = AppointmentRepository()
        appointment_date = datetime.now(timezone.utc) + timedelta(days=1)
        lock = repo.create_booking_lock('dr_a', appointment_date, 'Service A')
        db.session.flush()

        active = repo.get_active_booking_lock('dr_a', appointment_date)
        assert active is not None

        slots = repo.get_locked_time_slots('dr_a', appointment_date.date())
        assert appointment_date.replace(microsecond=0) in [d.replace(microsecond=0) for d in slots]

        repo.delete_booking_lock('dr_a', appointment_date)
        db.session.flush()

        assert repo.get_active_booking_lock('dr_a', appointment_date) is None
    finally:
        teardown_db(ctx)
