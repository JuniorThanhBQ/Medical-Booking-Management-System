from src.extensions import db
from src.modules.users.models import Profile, User


def get_user_by_email(email: str) -> User:
    return User.query.filter(User.email == email).first()


def add_user(user: User):
    db.session.add(user)
    db.session.flush()


def add_profile(profile: Profile):
    db.session.add(profile)


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()
