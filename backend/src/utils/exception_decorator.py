import logging
from functools import wraps

from sqlalchemy.exc import (DataError, IntegrityError, OperationalError,
                            SQLAlchemyError)

from src.extensions import db


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
