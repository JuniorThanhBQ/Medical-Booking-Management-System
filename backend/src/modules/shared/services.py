from datetime import date, datetime, timedelta


def parse_appointment_datetime(str_appointment_date=None):
    try:
        appointment_datetime = datetime.strptime(
            str_appointment_date.replace("Z", "").split(".")[0],
            "%Y-%m-%dT%H:%M:%S"
        )

        return appointment_datetime, None

    except ValueError:
        return None, ({"message": "Định dạng ngày không hợp lệ"}, "ERROR_BAD_REQUEST")


def validate_appointment_date(appointment_datetime=None):
    target_date = appointment_datetime.date()
    today = date.today()

    if target_date < today or target_date > (today + timedelta(days=30)):
        return {"message": "Chỉ được đặt lịch trong 30 ngày tới"}, "ERROR_BAD_REQUEST"

    return None, None


def validate_available_slot(appointment_datetime=None, available_slots=None):
    booked_slot = appointment_datetime.isoformat() + "Z"

    if booked_slot not in available_slots:
        return {"message": "Khung giờ không khả dụng"}, "ERROR_BAD_REQUEST"

    return None, None


def format_appointment(appointment=None, doctor=None, patient_user=None, patient_name=None, specialty=None):
    if patient_name is None:
        user = patient_user or appointment.patient_profile
        patient_name = f"{user.last_name} {user.first_name}"

    return {
        "id": appointment.id,
        "service": appointment.medical_service.name if appointment.medical_service else None,
        "name": appointment.name,
        "patientName": patient_name,
        "doctorName": f"{doctor.last_name} {doctor.first_name}" if doctor else None,
        "specialty": specialty if specialty else None,
        "appointmentDate": appointment.appointment_date.isoformat() + "Z",
        "status": appointment.status.name if appointment.status else None,
        "note": appointment.note,
        "createdAt": appointment.created_date.isoformat() + "Z",
        "updatedAt": appointment.updated_date.isoformat() + "Z",
    }


def check_is_conflicting(slot_start, duration, appointments):
    if isinstance(duration, int):
        duration_td = timedelta(minutes=duration)
    else:
        duration_td = duration

    slot_end = slot_start + duration_td

    for appointment in appointments:
        appointment_start = appointment.appointment_date

        if appointment.medical_service and appointment.medical_service.visit_type:
            visit_type = appointment.medical_service.visit_type
            appointment_duration_minutes = (visit_type.duration_minutes
                                            + visit_type.buffer_before
                                            + visit_type.buffer_after)
        else:
            appointment_duration_minutes = 30

        appointment_end = appointment_start + timedelta(minutes=appointment_duration_minutes)

        if slot_start < appointment_end and slot_end > appointment_start:
            return True

    return False


def format_speciality_output(specialty=None):
    return {
        "id": specialty.id,
        "name": specialty.name,
        "description": specialty.description,
        "level": specialty.level,
        "images": specialty.images if specialty.images else None
    }
