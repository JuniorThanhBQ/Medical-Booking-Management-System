import hashlib
from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests

GOOGLE_CLIENT_ID = "1234567890-abcxyz.apps.googleusercontent.com"

def verify_google_token(token):
    try:
        idinfo = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID
        )
        return idinfo
    except Exception:
        return None

def hashlib_password(password):
    return hashlib.md5(password.strip().encode("utf-8")).hexdigest()


def process_date_appointment(date, time):
    start_time_str = time.split("-")[0].strip()
    start_time_str = start_time_str.replace("h", ":")
    time_part = datetime.strptime(start_time_str, "%H:%M").time()
    return datetime.combine(date, time_part)


def get_total_money(
    treatment_services=None, appointment_service=None, medicine_record_info=None
):
    total_money = 0
    total_money += appointment_service.total

    for service in treatment_services:
        total_money += service.medical_service.total

    if medicine_record_info:
        for m in medicine_record_info:
            total_money += m.total

    return total_money


def datetime_formatter(view, context, model, name):
    if model.created_date:
        return model.created_date.strftime("%H:%M - %d/%m/%Y")
    return ""


def date_formatter(view, context, model, name):
    if model.birthday:
        return model.birthday.strftime("%d/%m/%Y")
    return ""
