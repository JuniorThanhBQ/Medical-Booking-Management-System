from tests.test_base import create_app
from src.extensions import db

from src.modules.users.repositories import UserRepository
from src.modules.users.models import User, Profile, UserRole


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


def test_add_and_get_user_by_email():
    ctx = setup_db()
    try:
        repo = UserRepository()
        u = User(username='u1', password='p', email='u1@example.com', first_name='F', last_name='L', role=UserRole.PATIENT)
        repo.add_user(u)
        db.session.flush()

        found = repo.get_user_by_email('u1@example.com')
        assert found is not None
        assert found.email == 'u1@example.com'
    finally:
        teardown_db(ctx)


def test_get_user_by_id_and_activate():
    ctx = setup_db()
    try:
        repo = UserRepository()
        u = User(username='u2', password='p', email='u2@example.com', first_name='F', last_name='L', role=UserRole.PATIENT, is_active=False)
        db.session.add(u)
        db.session.flush()

        got = repo.get_user_by_id(u.id)
        assert got.email == 'u2@example.com'

        assert repo.active_user_by_email('u2@example.com') is True
        assert repo.get_user_by_email('u2@example.com').is_active is True
    finally:
        teardown_db(ctx)


def test_activate_nonexistent_user_returns_false():
    ctx = setup_db()
    try:
        repo = UserRepository()
        assert repo.active_user_by_email('noone@example.com') is False
    finally:
        teardown_db(ctx)
