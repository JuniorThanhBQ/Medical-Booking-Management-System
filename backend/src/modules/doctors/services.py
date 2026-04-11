from datetime import date, datetime, timedelta

from sqlalchemy import func

from src.modules.appointments.models import Appointment, StatusRole
from src.modules.doctors.models import DayOfWeek
from src.modules.doctors.repositories import (commit_session, get_doctor_by_id,
                                              get_medical_service_by_id,
                                              get_or_create_work_schedule,
                                              get_paginated_doctors,
                                              get_paginated_medical_services,
                                              get_paginated_specialties,
                                              get_specialty_by_id,
                                              get_upcoming_appointments,
                                              is_conflict_appointment,
                                              update_work_dates)
from src.modules.shared.services import (check_is_conflicting,
                                         format_appointment,
                                         format_speciality_output)
from src.utils.handle_db_errors import handle_db_errors


@handle_db_errors
def get_my_schedule_service(current_user):
    if current_user.role.name != "DOCTOR":
        return {"message": "Chỉ bác sĩ mới có quyền truy cập"}, "FORBIDDEN"

    profile = current_user.profile
    if not profile or profile.profile_type != "doctor":
        return {"message": "Hồ sơ bác sĩ không hợp lệ"}, "NOT_FOUND"

    work_schedule_data = None
    if profile.work_schedule:
        work_schedule = profile.work_schedule
        work_schedule_data = {
            "title": work_schedule.title,
            "description": work_schedule.description,
            "startTime": work_schedule.start_time.strftime("%H:%M:%S") if work_schedule.start_time else None,
            "endTime": work_schedule.end_time.strftime("%H:%M:%S") if work_schedule.end_time else None,
            "workDate": [wd.day_of_week.name.capitalize() for wd in work_schedule.work_dates],
        }

    now = datetime.now()
    statuses = [StatusRole.APPROVED, StatusRole.PENDING]
    upcoming_appointments = get_upcoming_appointments(profile.id, now, statuses)

    appointment_data = [
        format_appointment(appointment=app, patient_user=app.patient.user, doctor=current_user)
        for app in upcoming_appointments
    ]

    result = {
        "workSchedule": work_schedule_data,
        "appointments": appointment_data
    }
    return result, "SUCCESS"


@handle_db_errors
def request_schedule_change_service(current_user, data):
    if current_user.role.name not in ["DOCTOR", "RECEPTIONIST", "ADMIN"]:
        return {"message": "Không đủ quyền hạn để yêu cầu đổi lịch"}, "FORBIDDEN"

    profile = current_user.profile
    if not profile or profile.profile_type != "doctor":
        return {"message": "Hồ sơ bác sĩ không hợp lệ"}, "NOT_FOUND"

    now = datetime.now()
    end_date = now + timedelta(days=30)
    statuses = [StatusRole.APPROVED, StatusRole.PENDING]

    conflicting = is_conflict_appointment(profile.id, now, end_date, statuses)

    if conflicting:
        return {"message": "Vui lòng cập nhật các lịch hẹn bị ảnh hưởng truớc khi đổi."}, "FORBIDDEN"

    new_work_schedule_data = data.get("newWorkSchedule", {})
    if not new_work_schedule_data:
        return {"message": "Thiếu thông tin lịch làm việc mới"}, "ERROR_BAD_REQUEST"

    try:
        start_time = datetime.strptime(new_work_schedule_data.get("start_time", "00:00:00"), "%H:%M:%S").time()
        end_time = datetime.strptime(new_work_schedule_data.get("end_time", "00:00:00"), "%H:%M:%S").time()
    except ValueError:
        return {"message": "Định dạng không hợp lệ (HH:MM:SS)"}, "ERROR_BAD_REQUEST"

    work_schedule = get_or_create_work_schedule(profile.id)
    work_schedule.title = new_work_schedule_data.get("title", work_schedule.title)
    work_schedule.description = new_work_schedule_data.get("description", work_schedule.description)
    work_schedule.start_time = start_time
    work_schedule.end_time = end_time

    work_days = new_work_schedule_data.get("work_date", [])
    days_enum = []
    for day_str in work_days:
        try:
            days_enum.append(DayOfWeek[day_str.upper()])
        except KeyError:
            pass

    update_work_dates(work_schedule.id, days_enum)
    commit_session()

    return {"message": "Cập nhật lịch thành công!"}, "SUCCESS"


@handle_db_errors
def get_specialties_service(page=1, per_page=10, keywords=None):
    pagination = get_paginated_specialties(page, per_page, keywords)
    items = [format_speciality_output(specialty) for specialty in pagination.items]

    result = {
        "items": items,
        "meta": {
            "total": pagination.total,
            "pages": pagination.pages,
            "currentPage": pagination.page,
            "perPage": pagination.per_page,
            "hasNext": pagination.has_next,
            "hasPrev": pagination.has_prev
        }
    }
    return result, "SUCCESS"


@handle_db_errors
def get_doctors_service(page=1, per_page=10, keywords=None, specialty_id=None, work_dates=None):
    pagination = get_paginated_doctors(page, per_page, keywords, specialty_id, work_days=work_dates)
    items = []

    for doctor in pagination.items:
        profile = doctor.profile
        items.append({
            "id": profile.id,
            "firstName": doctor.first_name,
            "lastName": doctor.last_name,
            "avatar": profile.avatar,
            "gender": profile.gender.name if profile.gender else None,
            "title": profile.title,
            "specialtyId": profile.specialty_id,
            "bio": profile.bio,
        })

    result = {
        "items": items,
        "meta": {
            "total": pagination.total,
            "pages": pagination.pages,
            "currentPage": pagination.page,
            "perPage": pagination.per_page,
            "hasNext": pagination.has_next,
            "hasPrev": pagination.has_prev
        }
    }
    return result, "SUCCESS"


@handle_db_errors
def get_medical_services_service(page=1, per_page=10, keywords=None, specialty_id=None):
    pagination = get_paginated_medical_services(page, per_page, keywords, specialty_id)
    items = [{
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "specialtyId": service.specialty_id
    } for service in pagination.items]

    result = {
        "items": items,
        "meta": {
            "total": pagination.total,
            "pages": pagination.pages,
            "currentPage": pagination.page,
            "perPage": pagination.per_page,
            "hasNext": pagination.has_next,
            "hasPrev": pagination.has_prev
        }
    }
    return result, "SUCCESS"


@handle_db_errors
def get_medical_service_detail_service(service_id):
    service = get_medical_service_by_id(service_id)
    if not service:
        return {"message": "Không tồn tại dịch vụ này"}, "NOT_FOUND"

    result = {
        "id": service.id,
        "name": service.name,
        "description": service.description,
        "specialty": {
            "id": service.specialty.id,
            "name": service.specialty.name,
            "level": service.specialty.level
        } if service.specialty else None,
        "visitType": {
            "id": service.visit_type.id,
            "name": service.visit_type.name,
            "durationMinutes": service.visit_type.duration_minutes
        } if service.visit_type else None
    }
    return result, "SUCCESS"


@handle_db_errors
def get_specialty_detail_service(specialty_id):
    specialty = get_specialty_by_id(specialty_id)
    if not specialty:
        return {"message": "Không tồn tại chuyên khoa này"}, "NOT_FOUND"

    return format_speciality_output(specialty), "SUCCESS"


@handle_db_errors
def get_doctor_detail_service(doctor_id):
    doctor = get_doctor_by_id(doctor_id)
    if not doctor or not doctor.profile:
        return {"message": "Bác sĩ không tồn tại"}, "NOT_FOUND"

    profile = doctor.profile
    schedule_data = format_work_schedule(profile.work_schedule)

    result = {
        "id": profile.id,
        "firstName": doctor.first_name,
        "lastName": doctor.last_name,
        "email": doctor.email,
        "profile": {
            "avatar": profile.avatar,
            "dateOfBirth": profile.birthday.isoformat() if profile.birthday else None,
            "gender": profile.gender.name if profile.gender else None,
            "phone": profile.phone,
            "title": profile.title,
            "specialtyId": profile.specialty_id,
            "bio": profile.bio,
        },
        "workSchedule": schedule_data,
    }
    return result, "SUCCESS"


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


def get_booked_appointments(doctor_id, target_date):
    return Appointment.query.filter(
        Appointment.doctor_profile_id == doctor_id,
        func.date(Appointment.appointment_date) == target_date,
        Appointment.status.in_([StatusRole.APPROVED, StatusRole.COMPLETED])
    ).all()


def get_available_time_slots(doctor, target_date, medical_service):
    if not doctor.profile or doctor.profile.profile_type != "doctor":
        return []

    schedule = doctor.profile.work_schedule
    if not schedule:
        return []

    target_day_name = target_date.strftime('%A').upper()
    working_days = [work_schedule.day_of_week.name for work_schedule in schedule.work_dates]
    if target_day_name not in working_days:
        return []

    visit_type = medical_service.visit_type
    if not visit_type:
        return []

    duration = visit_type.duration_minutes + visit_type.buffer_before + visit_type.buffer_after

    appointments = get_booked_appointments(doctor.profile.id, target_date)
    current_date = datetime.combine(target_date, schedule.start_time)
    end_date = datetime.combine(target_date, schedule.end_time)
    now_date = datetime.now()
    available = []

    while current_date + timedelta(minutes=duration) <= end_date:
        if current_date <= now_date:
            current_date += timedelta(minutes=duration)
            continue

        if not check_is_conflicting(current_date, duration, appointments):
            available.append(current_date.isoformat() + "Z")

        current_date += timedelta(minutes=duration)

    return available


@handle_db_errors
def get_time_slots_service(doctor_id, date_str, service_id):
    max_day_searching = 30
    doctor = get_doctor_by_id(doctor_id)

    if not doctor or not doctor.profile:
        return {"message": "Bác sĩ không tồn tại"}, "NOT_FOUND"

    try:
        if date_str:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            target_date = date.today()
    except ValueError:
        return {"message": "Định dạng không hợp lệ (YYYY-MM-DD)"}, "ERROR_BAD_REQUEST"

    today = date.today()
    if target_date < today or target_date > (today + timedelta(days=max_day_searching)):
        return {"message": f"Chỉ xem được lịch trong vòng {max_day_searching} ngày tới"}, "ERROR_BAD_REQUEST"

    if not service_id:
        return {"message": "Thiếu mã dịch vụ"}, "ERROR_BAD_REQUEST"

    medical_service = get_medical_service_by_id(service_id)
    if not medical_service:
        return {"message": "Dịch vụ không tồn tại"}, "NOT_FOUND"

    profile = doctor.profile
    if profile.specialty_id != medical_service.specialty_id:
        return {"message": "Bác sĩ không cung cấp dịch vụ này"}, "ERROR_BAD_REQUEST"

    if profile.work_schedule:
        work_schedule = profile.work_schedule
        work_schedule_data = format_work_schedule(work_schedule)
    else:
        return {"message": "Bác sĩ không tồn tại"}, "404"

    available_slots = get_available_time_slots(doctor, target_date, medical_service)

    result = [
        {
            "workSchedule": work_schedule_data,
            "availableTimeSlots": available_slots,
        }
    ]
    return result, "SUCCESS"
