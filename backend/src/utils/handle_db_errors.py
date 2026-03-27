import logging
from functools import wraps

from sqlalchemy.exc import (DataError, IntegrityError, OperationalError,
                            SQLAlchemyError)
from werkzeug.exceptions import BadRequest, InternalServerError

from src.extensions import db

logger = logging.getLogger('flask_logger')


def handle_db_errors(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)

        except IntegrityError as e:
            db.session.rollback()
            logger.exception("Lỗi ràng buộc dữ liệu: %s", e)
            raise BadRequest("Dữ liệu vi phạm ACID!") from e

        except DataError as e:
            db.session.rollback()
            logger.exception("Lỗi định dạng dữ liệu: %s", e)
            raise BadRequest("Có vấn đề trong dữ liệu!") from e

        except OperationalError as e:
            db.session.rollback()
            logger.exception("Lỗi kết nối CSDL: %s", e)
            raise InternalServerError("Hệ thống mất kết nối cơ sở dữ liệu!") from e

        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception("Lỗi truy vấn SQL: %s", e)
            raise InternalServerError("Có lỗi xảy ra trong khi xử lý dữ liệu!") from e

    return wrapper
