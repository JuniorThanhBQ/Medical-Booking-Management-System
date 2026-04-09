from datetime import date, datetime, timedelta

from src.modules.doctors.models import CtaLabel


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

    if target_date < today or target_date > (today + timedelta(days=7)):
        return {"message": "Chỉ được đặt lịch trong 7 ngày tới"}, "ERROR_BAD_REQUEST"

    return None, None


def validate_available_slot(appointment_datetime=None, available_slots=None):
    booked_slot = appointment_datetime.isoformat() + "Z"

    if booked_slot not in available_slots:
        return {"message": "Khung giờ không khả dụng"}, "ERROR_BAD_REQUEST"

    return None, None


def format_appointment(appointment, doctor=None, patient_user=None, specialty=None, patient_name=None):
    if patient_name is None:
        user = patient_user or appointment.patient_profile.user
        patient_name = f"{user.last_name} {user.first_name}"

    if specialty is None and doctor:
        specialty = doctor.profile.specialty

    return {
        "id": appointment.id,
        "type": specialty.cta_label.name if specialty and specialty.cta_label else None,
        "name": appointment.name,
        "patientName": patient_name,
        "doctorName": f"{doctor.last_name} {doctor.first_name}" if doctor else None,
        "appointmentDate": appointment.appointment_date.isoformat() + "Z",
        "status": appointment.status.name if appointment.status else None,
        "note": appointment.note,
        "createdAt": appointment.created_date.isoformat() + "Z",
        "updatedAt": appointment.updated_date.isoformat() + "Z",
    }


def get_slot_duration(doctor_profile=None):
    specialty = doctor_profile.specialty
    cta_label = specialty.cta_label.name if specialty and specialty.cta_label else "CK1"

    mapping = {item.name: item.value for item in CtaLabel}
    hours = mapping.get(cta_label, 1)

    return timedelta(hours=hours)


def check_is_conflicting(slot_start=None, duration=None, appointments=None):
    buffer = timedelta(minutes=30)
    slot_end = slot_start + duration

    for appointment in appointments:
        start = appointment.appointment_date
        end = start + duration
        if (slot_end + buffer > start) and (end + buffer > slot_start):
            return True

    return False


def format_speciality_output(specialty=None):
    return {
        "id": specialty.id,
        "name": specialty.name,
        "description": specialty.description,
        "level": specialty.level,
        "ctaLabel": specialty.cta_label.name if specialty.cta_label else None
    }
