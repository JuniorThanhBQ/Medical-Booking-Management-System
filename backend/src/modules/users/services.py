import datetime
from functools import wraps

import jwt
from flask import current_app, jsonify, request

from src.modules.users.models import User, db
from src.utils.utils import verify_google_token


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"message": "Thiếu token"}), 401
        try:
            token_val = token.split(" ")[1] if " " in token else token
            data = jwt.decode(
                token_val, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = db.session.get(User, data["user_id"])
            if not current_user:
                return jsonify({"message": "User không tồn tại"}), 401
        except Exception:
            return jsonify({"message": "Token không hợp lệ hoặc đã hết hạn"}), 401
        return f(current_user, *args, **kwargs)

    return decorator


def create_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(hours=1),
    }
    token = jwt.encode(payload, current_app.config["SECRET_KEY"], algorithm="HS256")
    return token.decode("utf-8") if isinstance(token, bytes) else token


def login_google(google_token):
    user_info = verify_google_token(google_token)

    if not user_info:
        return None, "Invalid Google token"

    email = user_info.get("email")
    name = user_info.get("name")

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(username=email, email=email, first_name=name, role="PATIENT")
        db.session.add(user)
        db.session.commit()

    token = create_token(user.id)
    return token, None
