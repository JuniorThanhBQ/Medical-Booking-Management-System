from datetime import date, datetime, timedelta

from src.modules.appointments.services import get_available_time_slots
from src.modules.auth_profile.models import (CtaLabel, Profile, Specialty,
                                             User, UserRole)
from src.utils.exception_decorator import handle_db_errors
from src.utils.utils import format_speciality_output, format_work_schedule


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
        format_speciality_output(specialty) for specialty in pagination.items
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
def get_specialty_detail_service(specialty_id):
    specialty = Specialty.query.filter(Specialty.id == specialty_id).first()

    if not specialty:
        return {"message": "Không tồn tại chuyên khoa này"}, "NOT_FOUND"

    result = format_speciality_output(specialty)

    return result, "SUCCESS"


def get_doctor_by_id(doctor_id):
    return User.query.filter(
        User.is_active,
        User.id == doctor_id,
        User.role == UserRole.DOCTOR
    ).first()


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
