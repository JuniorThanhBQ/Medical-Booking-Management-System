from functools import wraps

import jwt
from flask import current_app, request

from src.extensions import db
from src.modules.users.models import User
from src.utils.utils import error_response


def auth_required(f):
    @wraps(f)
    def token_verifying(*args, **kwargs):
        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return error_response("Token không tồn tại hoặc sai định dạng", 401)

        try:
            token_val = token.split(" ")[1]
            secret_key = current_app.config.get("SECRET_KEY")
            data = jwt.decode(token_val, secret_key, algorithms=["HS256"])

            user_id = data.get("user_id")
            if not user_id:
                return error_response("Payload của Token không hợp lệ", 401)

            current_user = db.session.get(User, user_id)

            if not current_user:
                return error_response("Người dùng không tồn tại", 404)

            if not current_user.is_active:
                return error_response("Tài khoản đã bị khoá", 403)

        except jwt.ExpiredSignatureError:
            return error_response("Token đã hết hạn", 401)

        except jwt.InvalidTokenError:
            return error_response("Token không hợp lệ", 401)

        except Exception as e:
            current_app.logger.error(f"Lỗi xác thực: {str(e)}", exc_info=True)
            return error_response("Lỗi khi xác thực tài khoản", 500)

        return f(current_user, *args, **kwargs)

    return token_verifying
