from functools import wraps

import jwt
from flask import current_app, request

from src.extensions import db
from src.modules.auth_profiles.models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return {"message": "Token không đúng định dạng"}, 401

        try:
            token_val = token.split(" ")[1]
            secret_key = current_app.config.get("SECRET_KEY")
            data = jwt.decode(token_val, secret_key, algorithms=["HS256"])
            current_user = db.session.get(User, data["user_id"])

            if not current_user:
                return {"message": "User không tồn tại"}, 400

            if not current_user.is_active:
                return {"message": "Tài khoản bị khoá"}, 403

        except jwt.ExpiredSignatureError:
            return {"message": "Token đã hết hạn"}, 401

        except jwt.InvalidTokenError:
            return {"message": "Token không hợp lệ"}, 401

        return f(current_user, *args, **kwargs)

    return decorator
