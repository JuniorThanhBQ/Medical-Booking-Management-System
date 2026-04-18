from src.extensions import db
from src.modules.users.models import Profile, User


class UserRepository:
    def get_user_by_email(self, email: str) -> User:
        return User.query.filter(User.email == email).first()

    def get_user_by_id(self, user_id: int) -> User:
        return db.session.get(User, user_id)

    def active_user_by_email(self, email: str):
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_active = True
            try:
                db.session.commit()
                return True
            except Exception:
                db.session.rollback()
                return False

        return False

    def add_user(self, user: User):
        db.session.add(user)
        db.session.flush()

    def add_profile(self, profile: Profile):
        db.session.add(profile)

    def commit(self):
        db.session.commit()

    def rollback(self):
        db.session.rollback()
