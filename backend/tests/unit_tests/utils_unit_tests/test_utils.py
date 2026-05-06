import datetime
from tests.test_base import test_app, test_client
from flask import Flask, make_response

from src.modules.users.models import GenderRole
from src.utils.utils import (check_xss_violation, error_response,
                             format_api_response, generate_username,
                             get_http_status_code, parse_date, parse_gender,
                             set_auth_cookie, validate_email_password)


def test_validate_email_password_invalid_email():
    res = validate_email_password('not-an-email', 'Aa1!aaaaa')

    assert isinstance(res, dict)
    assert 'email' not in res


def test_validate_email_password_invalid_password():
    res = validate_email_password('test@example.com', 'short')

    assert isinstance(res, dict)


def test_validate_email_password_valid():
    res = validate_email_password('user@example.com', 'Aa1!aaaaa')

    assert res is None


def test_check_xss_violation_true_and_false():
    assert check_xss_violation(['<script>alert(1)</script>']) is True
    assert check_xss_violation(['normal text', None, 123]) is False


def test_generate_username_normalization():
    username = generate_username('Thành', 'Đặng')

    assert 'thanh' in username
    assert 'dang' in username


def test_get_http_status_code_and_error_response():
    assert get_http_status_code('NOT_FOUND') == 404

    data, code = error_response('oops', 500)

    assert code == 500
    assert data['status'] == 'error'


def test_format_api_response():
    ok_data, ok_code = format_api_response({'a': 1}, 'SUCCESS', success_code=201)

    assert ok_code == 201

    err_data, err_code = format_api_response({'error': 'x'}, 'NOT_FOUND')

    assert err_code == 404


def test_parse_date():
    dt, err = parse_date('2020-01-02')

    assert isinstance(dt, datetime.datetime)
    assert err is None

    dt2, err2 = parse_date('bad-format')

    assert dt2 is None
    assert isinstance(err2, str)


def test_parse_gender():
    assert parse_gender('male') == GenderRole.MALE
    assert parse_gender('unknown', default=GenderRole.OTHER) == GenderRole.OTHER


def test_set_auth_cookie():
    app = Flask(__name__)

    with app.test_request_context('/'):
        resp = make_response({'ok': True})
        resp = set_auth_cookie(resp, 'refresh-token-123')
        cookies = resp.headers.get_all('Set-Cookie')

        assert any('refresh_token=refresh-token-123' in c for c in cookies)
