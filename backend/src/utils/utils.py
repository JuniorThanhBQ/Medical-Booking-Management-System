import datetime
import re
import unicodedata

import cloudinary.uploader
import jwt
from flask import current_app

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#_\-?])[A-Za-z\d@#_\-?]{9,}$")
XSS_REGEX = re.compile(r"<[^>]*>")


def cloudinary_upload_process(avatar):
    upload_result = cloudinary.uploader.upload(avatar)
    return upload_result.get("secure_url")


def check_xss_violation(values):
    for value in values:
        if value and isinstance(value, str) and XSS_REGEX.search(value):
            return True
    return False


def get_http_status_code(status_type, default=400):
    mapping = {"SERVER_INTERNAL_ERROR": 500, "FORBIDDEN": 403, "NOT_FOUND": 404,
               "ERROR_UNAUTHORIZED": 401, "ERROR_BAD_REQUEST": 400}
    return mapping.get(status_type, default)


def get_request_data(request):
    data = request.get_json(silent=True)

    if data is None:
        data = request.form.to_dict()
        if request.files:
            data.update(request.files.to_dict())

    return data or {}


def format_api_response(data, status_type, success_code=200):
    if status_type != "SUCCESS":
        return data, get_http_status_code(status_type)
    return data, success_code


def validate_email_password(email, password):
    if not EMAIL_REGEX.match(email):
        return {"message": "Định dạng email không hợp lệ."}
    if password and not PASSWORD_REGEX.match(password):
        return {"message": "Định dạng mật khẩu không hợp lệ"}
    return None


def generate_username(first_name, last_name):
    raw_name = f"{first_name}{last_name}".lower().replace(" ", "")
    raw_name = raw_name.replace('đ', 'd')
    username = (unicodedata.normalize('NFKD', raw_name).
                encode('ascii', 'ignore').decode('utf-8'))

    return username


def create_token(user):
    user_payload = {
        "user_id": user.id,
        "role": user.role.name,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=12),
        "iat": datetime.datetime.now(datetime.timezone.utc),
    }

    secret_key = current_app.config.get("SECRET_KEY")
    token = jwt.encode(user_payload, secret_key, algorithm="HS256")
    return token
