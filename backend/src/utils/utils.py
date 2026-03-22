import logging
import os
import re

import cloudinary.uploader
from google.auth.transport import requests
from google.oauth2 import id_token

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
    mapping = {"SERVER_INTERNAL_ERROR": 500, "FORBIDDEN": 403, "NOT_FOUND": 400}
    return mapping.get(status_type, default)


def get_request_data(request):
    return request.get_json(silent=True) or (
        request.form.to_dict() if hasattr(request.form, 'to_dict') else request.form)


def format_api_response(data, status_type, success_code=200):
    if status_type != "SUCCESS":
        return data, get_http_status_code(status_type, default=400)
    return data, success_code


def validate_email_password(email, password):
    if not EMAIL_REGEX.match(email):
        return {"message": "Định dạng email không hợp lệ."}, 400
    if password and not PASSWORD_REGEX.match(password):
        return {"message": "Định dạng mật khẩu không hợp lệ"}, 400
    return None, None


def verify_google_token(token):
    try:
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
        )
        return id_info

    except Exception as ex:
        logging.error(f"Lỗi trong xác thực google token: {ex}")
        return None
