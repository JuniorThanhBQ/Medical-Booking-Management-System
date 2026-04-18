from datetime import date, timedelta


def validate_appointment_date(appointment_datetime=None):
    target_date = appointment_datetime.date()
    today = date.today()

    if target_date < today or target_date > (today + timedelta(days=30)):
        return {"message": "Chỉ được đặt lịch trong 30 ngày tới"}, "ERROR_BAD_REQUEST"

    return None, None


def validate_available_slot(appointment_datetime=None, available_slots=None):
    booked_slot = appointment_datetime.isoformat() + "+07:00"

    if booked_slot not in available_slots:
        return {"message": "Khung giờ không khả dụng"}, "ERROR_BAD_REQUEST"

    return None, None


def validate_doctor(doctor):
    if not doctor or doctor.role.name != "DOCTOR" or not doctor.is_active:
        return {"message": "Bác sĩ không hợp lệ"}, "ERROR_BAD_REQUEST"
    return None, None
