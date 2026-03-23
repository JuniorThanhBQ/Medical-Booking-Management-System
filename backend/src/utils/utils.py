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
    data = request.get_json(silent=True)

    if data is None:
        data = request.form.to_dict()
        if request.files:
            data.update(request.files.to_dict())

    return data or {}


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


    except ValueError as e:
        logging.error("Token Google không hợp lệ hoặc đã hết hạn: %s", e)
        return None


def format_appointment_summary(appointment, patient_user, doctor_user, specialty):
    return {
        "id": str(appointment.id),
        "type": specialty.cta_label.name if specialty and specialty.cta_label else None,
        "patientName": f"{patient_user.last_name} {patient_user.first_name}",
        "doctorName": f"{doctor_user.last_name} {doctor_user.first_name}",
        "appointmentDate": appointment.appointment_date.isoformat() + "Z",
        "status": appointment.status.name if appointment.status else None,
        "note": appointment.note,
        "createdAt":
            appointment.created_date.isoformat() + "Z" if appointment.created_date else None,
        "updatedAt":
            appointment.updated_date.isoformat() + "Z" if appointment.updated_date else None,
    }


def format_appointment_response(appointment, doctor, patient_name=None):
    if patient_name is None:
        patient_name = (f"{appointment.patient_profile.user.last_name} "
                        f"{appointment.patient_profile.user.first_name}")

    return {
        "id": str(appointment.id),
        "type": doctor.profile.specialty.cta_label.name,
        "patientName": patient_name,
        "doctorName": f"{doctor.last_name} {doctor.first_name}",
        "appointmentDate": appointment.appointment_date.isoformat() + "Z",
        "status": appointment.status.name,
        "note": appointment.note,
        "createdAt": appointment.created_date.isoformat() + "Z",
        "updatedAt": appointment.updated_date.isoformat() + "Z"
    }


def format_work_schedule(work_schedule):
    if not work_schedule:
        return None

    return {
        "title": work_schedule.title,
        "description": work_schedule.description,
        "startTime":
            work_schedule.start_time.strftime("%H:%M:%S") if work_schedule.start_time else None,
        "endTime":
            work_schedule.end_time.strftime("%H:%M:%S") if work_schedule.end_time else None,
        "workDate": [wd.day_of_week.name.capitalize() for wd in work_schedule.work_dates],
    }


def format_speciality_output(specialty):
    return {
        "id": specialty.id,
        "name": specialty.name,
        "description": specialty.description,
        "level": specialty.level,
        "ctaLabel": specialty.cta_label.name if specialty.cta_label else None
    }
