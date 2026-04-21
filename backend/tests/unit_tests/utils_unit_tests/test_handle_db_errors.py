from sqlalchemy.exc import (DataError, IntegrityError, OperationalError,
                            SQLAlchemyError)
from werkzeug.exceptions import BadRequest, InternalServerError

from src import extensions
from src.utils.handle_db_errors import handle_db_errors


def _make_func_raising(exc):
    def f(*a, **k):
        raise exc
    return f


from tests.test_base import test_app


def test_handle_db_errors_integrity(test_app):
    func = handle_db_errors(_make_func_raising(IntegrityError('s', None, None)))
    import pytest
    with pytest.raises(BadRequest):
        func()


def test_handle_db_errors_data(test_app):
    func = handle_db_errors(_make_func_raising(DataError('s', None, None)))
    import pytest
    with pytest.raises(BadRequest):
        func()


def test_handle_db_errors_operational(test_app):
    func = handle_db_errors(_make_func_raising(OperationalError('s', None, None)))
    import pytest
    with pytest.raises(InternalServerError):
        func()


def test_handle_db_errors_sqlalchemy(test_app):
    func = handle_db_errors(_make_func_raising(SQLAlchemyError('s')))
    import pytest
    with pytest.raises(InternalServerError):
        func()
