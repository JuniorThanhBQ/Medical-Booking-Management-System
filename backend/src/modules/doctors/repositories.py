from sqlalchemy import asc, func, or_

from src.extensions import db
from src.modules.appointments.models import Appointment
from src.modules.doctors.models import (DoctorProfile, MedicalService,
                                        Specialty, WorkDate, WorkSchedule)
from src.modules.users.models import Profile, User, UserRole


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


def get_paginated_medical_services(page, per_page, keywords=None, specialty_id=None):
    query = MedicalService.query
    if keywords:
        search = f"%{keywords}%"
        query = query.filter(MedicalService.__table__.c.name.ilike(search))

    if specialty_id:
        query = query.filter(MedicalService.specialty_id == specialty_id)

    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_medical_service_by_id(service_id):
    return MedicalService.query.filter(MedicalService.id == service_id).first()


def get_paginated_doctors(page, per_page, keywords=None, specialty_id=None, work_days=None):
    query = User.query.join(User.profile).join(DoctorProfile).join(WorkSchedule).join(WorkDate).filter(
        User.is_active,
        User.role == UserRole.DOCTOR,
        Profile.profile_type == "doctor"
    )
    if keywords:
        if keywords:
            search = f"%{keywords}%"
            full_name = func.concat(User.last_name, ' ', User.first_name)
            query = query.filter(
                or_(
                    User.__table__.c.first_name.ilike(search),
                    User.__table__.c.last_name.ilike(search),
                    full_name.ilike(search),
                )
            )

    if specialty_id:
        query = query.join(DoctorProfile).filter(DoctorProfile.specialty_id == specialty_id)

    if work_days:
        query = query.filter(WorkDate.day_of_week.in_(work_days))

    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_doctor_by_id(doctor_id):
    return User.query.join(DoctorProfile).join(WorkSchedule).filter(DoctorProfile.id == doctor_id).first()


def get_upcoming_appointments(doctor_profile_id, start_date, statuses):
    return Appointment.query.filter(
        Appointment.doctor_profile_id == doctor_profile_id,
        Appointment.appointment_date >= start_date,
        Appointment.status.in_(statuses)
        ).order_by(asc(Appointment.__table__.c.appointment_date))


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
        work_schedule = WorkSchedule(doctor_id=doctor_id)
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
