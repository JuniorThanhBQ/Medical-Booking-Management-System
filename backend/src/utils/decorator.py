import logging
from functools import wraps

import jwt
from flask import current_app, request
from sqlalchemy.exc import (DataError, IntegrityError, OperationalError,
                            SQLAlchemyError)

from src.extensions import db
from src.modules.auth_profile.models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return {"message": "Có vấn đề trong xác thực token"}, 401

        try:
            token_val = token.split(" ")[1]
            secret_key = current_app.config.get("SECRET_KEY") or ("fake-key" * 5)
            data = jwt.decode(token_val, secret_key, algorithms=["HS256"])
            current_user = db.session.get(User, data["user_id"])

            if not current_user:
                return {"message": "User không tồn tại"}, 401

        except jwt.ExpiredSignatureError:
            return {"message": "Token đã hết hạn"}, 401

        except jwt.InvalidTokenError:
            return {"message": "Token không hợp lệ"}, 401

        return f(current_user, *args, **kwargs)

    return decorator


def handle_db_errors(parameter=3):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)

            except IntegrityError as e:
                db.session.rollback()
                logging.error("Lỗi ràng buộc dữ liệu: %s", e)
                message = "Dữ liệu đã tồn tại hoặc vi phạm toàn vẹn!"
                status = "ERROR_BAD_REQUEST"

            except DataError as e:
                db.session.rollback()
                logging.error("Lỗi định dạng dữ liệu: %s", e)
                message = "Dữ liệu thực thi có vấn đề!"
                status = "ERROR_BAD_REQUEST"

            except OperationalError as e:
                db.session.rollback()
                logging.error("Lỗi kết nối CSDL: %s", e)
                message = "Có vấn đề trong kết nối CSDL!"
                status = "SERVER_INTERNAL_ERROR"

            except SQLAlchemyError as e:
                db.session.rollback()
                logging.error("Lỗi truy vấn SQL: %s", e)
                message = "Có lỗi khi lấy dữ liệu!"
                status = "SERVER_INTERNAL_ERROR"

            if parameter == 2:
                return None, message

            if parameter == 4:
                return None, message, None, status

            return None, message, status

        return wrapper

    return decorator
