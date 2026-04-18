import datetime

import jwt
from flask import current_app
from itsdangerous import URLSafeTimedSerializer


def generate_token(user, expires_delta):
    if not user:
        return None

    now = datetime.datetime.now(datetime.timezone.utc)
    user_payload = {
        "user_id": user.id,
        "role": user.role.name,
        "iat": now,
        "exp": now + expires_delta,
    }

    secret_key = current_app.config.get("SECRET_KEY")
    token = jwt.encode(user_payload, secret_key, algorithm="HS256")
    return token


def create_token(user=None):
    return generate_token(user, datetime.timedelta(hours=12))


def create_refresh_token(user=None):
    return generate_token(user, datetime.timedelta(days=7))


def generate_verification_token(email: str) -> str:
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    salt = current_app.config.get('SECURITY_PASSWORD_AUTH')
    return serializer.dumps(email, salt=salt)


def confirm_verification_token(token: str, expiration=900):
    serializer = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        salt = current_app.config.get('SECURITY_PASSWORD_AUTH')
        email = serializer.loads(token, salt=salt, max_age=expiration)
        return email
    except Exception:
        return False
