import datetime
import re
import unicodedata

from flask import make_response

from src.modules.users.models import GenderRole

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^a-zA-Z0-9\s])\S{9,}$")
XSS_REGEX = re.compile(r"<[^>]{0,2000}>")


def validate_email_password(email, password):
    if not EMAIL_REGEX.match(email):
        return {"message": "Định dạng email không hợp lệ."}

    if password and not PASSWORD_REGEX.match(password):
        return {"message": "Định dạng mật khẩu không hợp lệ."}

    return None


def check_xss_violation(values):
    for value in values:
        if value and isinstance(value, str) and XSS_REGEX.search(value):
            return True

    return False


def generate_username(first_name, last_name):
    full_name = f"{first_name}{last_name}".lower().replace(" ", "")
    full_name = full_name.replace('đ', 'd')
    username = (unicodedata.normalize('NFKD', full_name).
                encode('ascii', 'ignore').decode('utf-8'))

    return username


def get_request_data(request):
    data = request.get_json(silent=True)

    if data is None:
        data = request.form.to_dict()
        if request.files:
            data.update(request.files.to_dict())

    return data or {}


def set_auth_cookie(response, refresh_token):
    response.set_cookie(
        "refresh_token",
        refresh_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=7 * 24 * 60 * 60
    )
    return response


def handle_auth_refresh_response(data, status, success_code=200, refresh_token=None):
    response_data = format_api_response(data, status, success_code=success_code)
    res = make_response(response_data)

    if status == "SUCCESS" and refresh_token:
        set_auth_cookie(res, refresh_token)

    return res


def get_http_status_code(status_type, default=400):
    mapping = {"SERVER_INTERNAL_ERROR": 500, "FORBIDDEN": 403, "NOT_FOUND": 404,
               "ERROR_UNAUTHORIZED": 401, "ERROR_BAD_REQUEST": 400, "CONFLICT": 409}

    return mapping.get(status_type, default)


def error_response(message: str, code: int):
    return {
        "status": "error",
        "code": code,
        "message": message
    }, code


def format_api_response(data, status_type, success_code=200):
    if status_type != "SUCCESS":
        return data, get_http_status_code(status_type)

    return data, success_code


def parse_date(date_str):
    if not date_str:
        return None, None
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d"), None
    except ValueError:
        return None, "Sai định dạng ngày sinh"


def parse_gender(gender_str, default: GenderRole = GenderRole.NOT_SET):
    if not gender_str:
        return default
    try:
        return GenderRole[gender_str.upper()]
    except KeyError:
        return default
