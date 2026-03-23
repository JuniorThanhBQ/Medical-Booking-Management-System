from datetime import date, datetime, timedelta

from sqlalchemy import func

from src.modules.appointments.models import Appointment, StatusRole
from src.modules.auth_profile.models import Specialty, User, UserRole, Profile, CtaLabel
from src.utils.decorator import handle_db_errors


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


@handle_db_errors(parameter=2)
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

    items = [
        {
            "id": specialty.id,
            "name": specialty.name,
            "description": specialty.description,
            "level": specialty.level,
            "ctaLabel": specialty.cta_label.name if specialty.cta_label else None,
        } for specialty in pagination.items
    ]

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


@handle_db_errors(parameter=2)
def get_doctors_service(page=1, per_page=10, keywords=None, specialty_id=None):
    query = User.query.join(User.profile).filter(
        User.is_active == True,
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
                "id": doctor.id,
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


def get_doctor_by_id(doctor_id):
    return User.query.filter(
        User.is_active == True,
        User.id == doctor_id,
        User.role == UserRole.DOCTOR
    ).first()


@handle_db_errors(parameter=2)
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
        "id": doctor.id,
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


@handle_db_errors(parameter=2)
def get_time_slots_service(doctor_id, date_str):
    doctor = get_doctor_by_id(doctor_id)

    if not doctor or not doctor.profile:
        return {"message": "Bác sĩ không tồn tại"}, "NOT_FOUND"

    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else date.today()
    except ValueError:
        return {"message": "Định dạng không hợp lệ (YYYY-MM-DD)"}, "ERROR_BAD_REQUEST"

    today = date.today()
    if target_date < today or target_date > (today + timedelta(days=7)):
        return {"message": "Chỉ xem được lịch trống trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"

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


def get_available_time_slots(doctor, target_date):
    if not doctor.profile or doctor.profile.profile_type != "doctor":
        return []

    schedule = doctor.profile.work_schedule
    if not schedule:
        return []

    target_day_name = target_date.strftime('%A').upper()
    if not any(wd.day_of_week.name == target_day_name for wd in schedule.work_dates):
        return []

    if doctor.profile.specialty and doctor.profile.specialty.cta_label:
        specialty_cta = doctor.profile.specialty.cta_label.name
    else:
        specialty_cta = "CK1"

    hours = 1
    if specialty_cta == "CK2":
        hours = 2
    elif specialty_cta == "CK3":
        hours = 3
    duration = timedelta(hours=hours)

    appointments = Appointment.query.filter(
        Appointment.doctor_profile_id == doctor.profile.id,
        func.date(Appointment.appointment_date) == target_date,
        Appointment.status.in_([StatusRole.APPROVED, StatusRole.COMPLETED])
    ).all()

    available = []
    curr_dt = datetime.combine(target_date, schedule.start_time)
    end_dt = datetime.combine(target_date, schedule.end_time)
    now_dt = datetime.now()

    while curr_dt + duration <= end_dt:
        if curr_dt <= now_dt:
            curr_dt += timedelta(minutes=30)
            continue

        conflict = False
        for a in appointments:
            a_start = a.appointment_date
            a_end = a_start + duration
            if ((curr_dt + duration + timedelta(minutes=30) > a_start)
                    and (a_end + timedelta(minutes=30) > curr_dt)):
                conflict = True
                break

        if not conflict:
            available.append(curr_dt.isoformat() + "Z")

        curr_dt += timedelta(minutes=30)

    return available
