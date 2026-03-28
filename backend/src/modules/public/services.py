from datetime import date, datetime, timedelta

from sqlalchemy import func

from src.modules.appointments.models import Appointment, StatusRole
from src.modules.auth_profiles.models import (CtaLabel, DoctorProfile, Profile,
                                              Specialty, User, UserRole)
from src.modules.shared.services import get_slot_duration, is_conflicting
from src.utils.handle_db_errors import handle_db_errors


@handle_db_errors
def get_specialties_service(page=1, per_page=10, keywords=None, cta_label=None):
    query = Specialty.query

    if keywords:
        query = query.filter(
            Specialty.name.ilike(f"%{keywords}%") | Specialty.description.ilike(f"%{keywords}%")
        )

    if cta_label:
        try:
            query = query.filter(Specialty.cta_label == CtaLabel[cta_label])
        except KeyError:
            pass

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

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
def get_doctors_service(page=1, per_page=10, keywords=None, specialty_id=None):
    query = User.query.join(User.profile).filter(
        User.is_active,
        User.role == UserRole.DOCTOR,
        Profile.profile_type == "doctor"
    )

    if keywords:
        query = query.filter(
            User.first_name.ilike(f"%{keywords}%") |
            User.last_name.ilike(f"%{keywords}%")
        )

    if specialty_id:
        query = query.filter(Profile.specialty_id == specialty_id)

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    items = []

    for doctor in pagination.items:
        profile = doctor.profile
        items.append(
            {
                "id": profile.id,
                "firstName": doctor.first_name,
                "lastName": doctor.last_name,
                "avatar": profile.avatar,
                "gender": profile.gender.name if profile.gender else None,
                "title": profile.title,
                "specialtyId": profile.specialty_id,
                "bio": profile.bio,
            }
        )

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
def get_specialty_detail_service(specialty_id):
    specialty = Specialty.query.filter(Specialty.id == specialty_id).first()

    if not specialty:
        return {"message": "Không tồn tại chuyên khoa này"}, "NOT_FOUND"

    result = format_speciality_output(specialty)

    return result, "SUCCESS"


def format_speciality_output(specialty):
    return {
        "id": specialty.id,
        "name": specialty.name,
        "description": specialty.description,
        "level": specialty.level,
        "ctaLabel": specialty.cta_label.name if specialty.cta_label else None
    }


@handle_db_errors
def get_doctor_detail_service(doctor_id):
    doctor = get_doctor_by_id(doctor_id)

    if not doctor or not doctor.profile:
        return {"message": "Bác sĩ không tồn tại"}, "NOT_FOUND"

    profile = doctor.profile
    schedule_data = None

    if profile.work_schedule:
        work_schedule = profile.work_schedule
        schedule_data = format_work_schedule(work_schedule)

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


def get_booked_appointments(doctor_id, target_date):
    return Appointment.query.filter(
        Appointment.doctor_profile_id == doctor_id,
        func.date(Appointment.appointment_date) == target_date,
        Appointment.status.in_([StatusRole.APPROVED, StatusRole.COMPLETED])
    ).all()


def get_available_time_slots(doctor, target_date):
    if not doctor.profile or doctor.profile.profile_type != "doctor":
        return []

    schedule = doctor.profile.work_schedule
    if not schedule:
        return []

    target_day_name = target_date.strftime('%A').upper()
    working_days = [work_schedule.day_of_week.name for work_schedule in schedule.work_dates]
    if target_day_name not in working_days:
        return []

    duration = get_slot_duration(doctor.profile)
    appointments = get_booked_appointments(doctor.profile.id, target_date)
    current_date = datetime.combine(target_date, schedule.start_time)
    end_date = datetime.combine(target_date, schedule.end_time)
    now_date = datetime.now()
    available = []

    while current_date + duration <= end_date:
        if current_date <= now_date:
            current_date += timedelta(minutes=30)
            continue

        if not is_conflicting(current_date, duration, appointments):
            available.append(current_date.isoformat() + "Z")

        current_date += timedelta(minutes=30)

    return available


def get_doctor_by_id(doctor_id):
    return User.query.join(DoctorProfile).filter(DoctorProfile.id == doctor_id).first()


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
        "workDate": [work_schedule.day_of_week.name.capitalize()
                     for work_schedule in work_schedule.work_dates],
    }


@handle_db_errors
def get_time_slots_service(doctor_id, date_str):
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
    if target_date < today or target_date > (today + timedelta(days=7)):
        return {"message": "Chỉ xem được lịch trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"

    profile = doctor.profile
    work_schedule_data = None

    if profile.work_schedule:
        work_schedule = profile.work_schedule
        work_schedule_data = format_work_schedule(work_schedule)

    available_slots = get_available_time_slots(doctor, target_date)

    result = [
        {
            "workSchedule": work_schedule_data,
            "availableTimeSlots": available_slots,
        }
    ]
    return result, "SUCCESS"
