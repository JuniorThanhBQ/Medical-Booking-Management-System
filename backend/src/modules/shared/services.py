from datetime import date, datetime, timedelta


def parse_appointment_datetime(str_appointment_date):
    try:
        appointment_datetime = datetime.strptime(
            str_appointment_date.replace("Z", "").split(".")[0],
            "%Y-%m-%dT%H:%M:%S"
        )

        return appointment_datetime, None

    except ValueError:
        return None, ({"message": "Định dạng ngày không hợp lệ"}, "ERROR_BAD_REQUEST")


def validate_appointment_date(appointment_datetime):
    target_date = appointment_datetime.date()
    today = date.today()

    if target_date < today or target_date > (today + timedelta(days=7)):
        return {"message": "Chỉ được đặt lịch trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"

    return None, None


def validate_available_slot(appointment_datetime, available_slots):
    exact_iso = appointment_datetime.isoformat() + "Z"

    if exact_iso not in available_slots:
        return {"message": "Khung giờ này không khả dụng hoặc đã có người đặt"}, "ERROR_BAD_REQUEST"

    return None, None


def format_appointment_summary(appointment, patient_user, doctor_user, specialty):
    return {
        "id": str(appointment.id),
        "type": specialty.cta_label.name if specialty and specialty.cta_label else None,
        "name": appointment.name,
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
        "name": appointment.name,
        "patientName": patient_name,
        "doctorName": f"{doctor.last_name} {doctor.first_name}",
        "appointmentDate": appointment.appointment_date.isoformat() + "Z",
        "status": appointment.status.name,
        "note": appointment.note,
        "createdAt": appointment.created_date.isoformat() + "Z",
        "updatedAt": appointment.updated_date.isoformat() + "Z"
    }


def get_slot_duration(doctor_profile):
    specialty = doctor_profile.specialty
    cta_label = specialty.cta_label.name if specialty and specialty.cta_label else "CK1"

    mapping = {"CK1": 1, "CK2": 2, "CK3": 3}
    hours = mapping.get(cta_label, 1)
    return timedelta(hours=hours)


def is_conflicting(slot_start, duration, appointments):
    buffer = timedelta(minutes=30)
    slot_end = slot_start + duration

    for a in appointments:
        a_start = a.appointment_date
        a_end = a_start + duration
        if (slot_end + buffer > a_start) and (a_end + buffer > slot_start):
            return True
    return False
