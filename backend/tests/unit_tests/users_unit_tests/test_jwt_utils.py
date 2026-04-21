import datetime

import jwt
from flask import Flask

from src.utils.users import jwt_utils
from tests.test_base import test_app


class DummyRole:
    def __init__(self, name):
        self.name = name


class DummyUser:
    def __init__(self, id, role):
        self.id = id
        self.role = role


def test_generate_and_decode_token(test_app):
    app = test_app
    app.config['SECRET_KEY'] = 'x' * 32
    user = DummyUser(1, DummyRole('PATIENT'))

    token = jwt_utils.create_token(user)
    assert token is not None
    decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
    assert decoded['user_id'] == 1


def test_verification_token_roundtrip(test_app):
    app = test_app
    app.config['SECRET_KEY'] = 'y' * 32
    app.config['SECURITY_PASSWORD_AUTH'] = 'salt'

    token = jwt_utils.generate_verification_token('a@b.com')
    email = jwt_utils.confirm_verification_token(token)
    assert email == 'a@b.com'

    assert jwt_utils.confirm_verification_token('invalid-token') is False
