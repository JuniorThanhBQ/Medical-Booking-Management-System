from modules.users.services import login


def test_login_success():
    user = login("admin", "123")
    assert user is not None


def test_login_wrong_password():
    user = login("admin", "")
    assert user is None


def test_login_wrong_username():
    user = login("", "")
    assert user is None
