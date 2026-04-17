from datetime import time

from sqlalchemy import asc, func, or_

from src.extensions import db
from src.modules.appointments.models import Appointment
from src.modules.doctors.models import (DayOfWeek, DoctorProfile,
                                        MedicalService, Specialty, WorkDate,
                                        WorkSchedule)
from src.modules.users.models import User, UserRole


def get_paginated_specialties(page, per_page, keywords=None):
    query = Specialty.query
    if keywords:
        search = f"%{keywords}%"
        query = query.filter(
            or_(
                Specialty.__table__.c.name.ilike(search),
                Specialty.__table__.c.description.ilike(search)
            )
        )

    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_specialty_by_id(specialty_id):
    return Specialty.query.filter(Specialty.id == specialty_id).first()


def get_paginated_medical_services(page, per_page=5, keywords=None, specialty_id=None):
    query = MedicalService.query
    if keywords:
        search = f"%{keywords}%"
        query = query.filter(MedicalService.__table__.c.name.ilike(search))

    if specialty_id:
        query = query.filter(MedicalService.specialty_id == specialty_id)

    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_medical_service_by_id(service_id):
    return MedicalService.query.filter(MedicalService.id == service_id).first()

def get_doctor_ids_by_work_day(work_days):
    if not work_days:
        return []

    try:
        target_day = DayOfWeek[work_days.upper()]
    except KeyError:
        return []

    schedules = WorkSchedule.query.join(WorkDate, WorkSchedule.id == WorkDate.work_schedule_id
    ).filter(WorkDate.day_of_week == target_day).all()
    doctor_ids = []
    for sched in schedules:
        doc_id = sched.doctor_id
        if doc_id is not None:
            doctor_ids.append(doc_id)

    return list(set(doctor_ids))

def get_paginated_doctors(page, per_page, keywords=None, specialty_id=None, work_days=None):
    query = User.query.join(DoctorProfile, User.id == DoctorProfile.user_id)

    query = query.filter(
        User.is_active == True,
        User.role == UserRole.DOCTOR,
        DoctorProfile.profile_type == "doctor"
    )

    if work_days:
        valid_doctor_ids = get_doctor_ids_by_work_day(work_days)
        if not valid_doctor_ids:
            query = query.filter(DoctorProfile.id == -1)
        else:
            query = query.filter(DoctorProfile.id.in_(valid_doctor_ids))


    if keywords:
        search = f"%{keywords}%"
        full_name = func.concat(User.last_name, ' ', User.first_name)
        query = query.filter(
            or_(
                User.first_name.ilike(search),
                User.last_name.ilike(search),
                full_name.ilike(search)
            )
        )

    if specialty_id:
        query = query.filter(DoctorProfile.specialty_id == specialty_id)

    query = query.group_by(User.id)

    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_doctor_by_id(doctor_id):
    return User.query.outerjoin(DoctorProfile) \
        .outerjoin(WorkSchedule) \
        .filter(DoctorProfile.id == doctor_id) \
        .first()


def get_upcoming_appointments(doctor_profile_id, start_date, statuses):
    return Appointment.query.filter(
        Appointment.doctor_profile_id == doctor_profile_id,
        Appointment.appointment_date >= start_date,
        Appointment.status.in_(statuses)
    ).order_by(asc(Appointment.__table__.c.appointment_date)).all()


def is_conflict_appointment(doctor_profile_id, start_date, end_date, statuses):
    return Appointment.query.filter(
        Appointment.doctor_profile_id == doctor_profile_id,
        Appointment.appointment_date >= start_date,
        Appointment.appointment_date <= end_date,
        Appointment.status.in_(statuses)
    ).first()


def get_or_create_work_schedule(doctor_id):
    work_schedule = WorkSchedule.query.filter_by(doctor_id=doctor_id).first()
    if not work_schedule:
        work_schedule = WorkSchedule(doctor_id=doctor_id, title="", start_time=time(8, 0, 0),
                                     end_time=time(8, 0, 0))
        db.session.add(work_schedule)
        db.session.flush()
    return work_schedule


def update_work_dates(work_schedule_id, days_enum):
    WorkDate.query.filter_by(work_schedule_id=work_schedule_id).delete()
    db.session.flush()
    for day in days_enum:
        new_date = WorkDate(day_of_week=day, work_schedule_id=work_schedule_id)
        db.session.add(new_date)


def commit_session():
    db.session.commit()
