from tests.test_base import test_app,create_app, test_session
from src.extensions import db

from src.modules.users.repositories import UserRepository
from src.modules.users.models import User, Profile, UserRole

def test_add_and_get_user_by_email(test_session):
    repo = UserRepository()
    repo.add_user(User(username='u1', password='p', email='u1@example.com', first_name='F', last_name='L', role=UserRole.PATIENT))
    db.session.flush()

    u = User.query.filter_by(email='u1@example.com').first()

    assert u is not None
    assert u.email == 'u1@example.com'


def test_get_user_by_id_and_activate(test_session):
    repo = UserRepository()
    repo.add_user(
        User(id=1,username='u2', password='p', email='u2@example.com', first_name='F', last_name='L', role=UserRole.PATIENT, is_active=False))
    db.session.flush()

    u = User.query.filter_by(id=1).first()

    assert u is not None
    assert u.email == 'u2@example.com'
    assert u.is_active is False

    assert repo.active_user_by_email('u2@example.com') is True
    assert repo.get_user_by_email('u2@example.com').is_active is True


def test_activate_nonexistent_user_returns_false(test_session):
    repo = UserRepository()

    assert repo.active_user_by_email('noone@example.com') is False
