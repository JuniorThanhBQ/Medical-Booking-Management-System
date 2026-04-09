from datetime import datetime, timedelta

from src.extensions import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.doctors.models import (CtaLabel, DayOfWeek, DoctorProfile,
                                        Specialty, WorkDate, WorkSchedule)
from src.modules.shared.services import (format_appointment,
                                         format_speciality_output)
from src.modules.users.models import Profile, User, UserRole
from src.utils.handle_db_errors import handle_db_errors


@handle_db_errors
def get_my_schedule_service(current_user):
    if current_user.role.name != "DOCTOR":
        return {"message": "Chỉ bác sĩ mới có quyền truy cập"}, "FORBIDDEN"

    profile = current_user.profile
    if not profile or profile.profile_type != "doctor":
        return {"message": "Hồ sơ bác sĩ không hợp lệ"}, "NOT_FOUND"

    ws_data = None
    if profile.work_schedule:
        ws = profile.work_schedule
        ws_data = {
            "title": ws.title,
            "description": ws.description,
            "startTime": ws.start_time.strftime("%H:%M:%S") if ws.start_time else None,
            "endTime": ws.end_time.strftime("%H:%M:%S") if ws.end_time else None,
            "workDate": [work_schedule.day_of_week.name.capitalize()
                         for work_schedule in ws.work_dates],
        }

    now = datetime.now()
    upcoming_appointments = Appointment.query.filter(
        Appointment.doctor_profile_id == profile.id,
        Appointment.appointment_date >= now,
        Appointment.status.in_([StatusRole.APPROVED, StatusRole.PENDING])
    ).order_by(Appointment.appointment_date.asc()).all()

    appointment_data = []
    for appointment in upcoming_appointments:
        patient_user = appointment.patient.user
        doctor_user = current_user
        specialty = profile.specialty
        appointment_data.append(
            format_appointment(appointment, patient_user, doctor_user, specialty)
        )

    result = {
        "workSchedule": ws_data,
        "appointments": appointment_data
    }
    return result, "SUCCESS"


@handle_db_errors
def request_schedule_change_service(current_user, data):
    if current_user.role.name != "DOCTOR":
        return {"message": "Chỉ bác sĩ mới có quyền này"}, "FORBIDDEN"

    profile = current_user.profile
    if not profile or profile.profile_type != "doctor":
        return {"message": "Hồ sơ bác sĩ không hợp lệ"}, "NOT_FOUND"

    now = datetime.now()
    seven_days_later = now + timedelta(days=7)

    conflicting_appointments = Appointment.query.filter(
        Appointment.doctor_profile_id == profile.id,
        Appointment.appointment_date >= now,
        Appointment.appointment_date <= seven_days_later,
        Appointment.status.in_([StatusRole.APPROVED, StatusRole.PENDING])
    ).first()

    if conflicting_appointments:
        return {"message": "Có lịch hẹn ở trong phạm vi 7 ngày tới."}, "FORBIDDEN"

    new_ws_data = data.get("newWorkSchedule", {})
    if not new_ws_data:
        return {"message": "Thiếu thông tin lịch làm việc mới"}, "ERROR_BAD_REQUEST"

    try:
        start_time = datetime.strptime(new_ws_data.get("start_time", "00:00:00"), "%H:%M:%S").time()
        end_time = datetime.strptime(new_ws_data.get("end_time", "00:00:00"), "%H:%M:%S").time()
    except ValueError:
        return {"message": "Định dạng không hợp lệ (HH:MM:SS)"}, "ERROR_BAD_REQUEST"

    ws = profile.work_schedule
    if not ws:
        ws = WorkSchedule(doctor_id=profile.id)
        db.session.add(ws)

    ws.title = new_ws_data.get("title", ws.title)
    ws.description = new_ws_data.get("description", ws.description)
    ws.start_time = start_time
    ws.end_time = end_time

    WorkDate.query.filter_by(work_schedule_id=ws.id).delete()
    db.session.flush()

    work_days = new_ws_data.get("work_date", [])
    for day_str in work_days:
        try:
            day_enum = DayOfWeek[day_str.upper()]
            new_work_schedule = WorkDate(day_of_week=day_enum, work_schedule_id=ws.id)
            db.session.add(new_work_schedule)
        except KeyError:
            pass

    db.session.commit()
    return {"message": "Đã gửi yêu cầu đổi lịch"}, "SUCCESS"


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
        query = query.join(DoctorProfile).filter(DoctorProfile.specialty_id == specialty_id)

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
