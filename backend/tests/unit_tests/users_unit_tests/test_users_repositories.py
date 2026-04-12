from src.modules.users.models import PatientProfile, User
from src.modules.users.repositories import (add_profile, add_user, commit,
                                            get_user_by_email, rollback)
from tests.test_base import test_app, test_session


def test_user_repositories(test_app, test_session):
    with test_app.app_context():
        new_user = User(
            username="repo_user",
            password="hashed_password",
            email="repo@test.com",
            first_name="Repo",
            last_name="Test"
        )
        add_user(new_user)
        commit()

        fetched_user = get_user_by_email("repo@test.com")
        assert fetched_user is not None
        assert fetched_user.username == "repo_user"

        new_profile = PatientProfile(
            user_id=fetched_user.id,
            phone="0123456789"
        )
        add_profile(new_profile)
        commit()
        assert fetched_user.profile.phone == "0123456789"

        fail_user = User(
            username="fail_user",
            password="pwd",
            email="fail@test.com",
            first_name="Fail",
            last_name="Test"
        )
        add_user(fail_user)
        rollback()

        assert get_user_by_email("fail@test.com") is None