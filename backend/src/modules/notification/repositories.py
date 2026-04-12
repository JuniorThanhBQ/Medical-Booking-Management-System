from datetime import datetime, time, timedelta

from sqlalchemy import desc

from src.extensions import db
from src.modules.appointments.models import Appointment
from src.modules.doctors.models import DoctorProfile
from src.modules.notification.models import DeliveryStatus, Notification
from src.modules.users.models import PatientProfile, User


def get_paginated_by_user_id(user_id, page=1, per_page=5):
    return (Notification.query.filter_by(user_id=user_id).order_by(desc("created_date")).
            paginate(page=page, per_page=per_page, error_out=False))


def get_notification_by_id(notification_id):
    return Notification.query.get(notification_id)


def get_unread_by_user_id(user_id):
    return Notification.query.filter_by(user_id=user_id, is_read=False).all()


def get_by_id_and_user_id(notification_id, user_id):
    return Notification.query.filter_by(id=notification_id, user_id=user_id).first()


def commit():
    db.session.commit()


def rollback():
    db.session.rollback()


def bulk_mark_as_read(notifications):
    for notification in notifications:
        notification.is_read = True
    db.session.commit()


def delete_notification(notification):
    db.session.delete(notification)
    db.session.commit()


def update_email_status(notification, status):
    notification.email_status = status
    db.session.commit()


def add_and_commit_notification(notification):
    db.session.add(notification)
    db.session.commit()
    return notification


def get_appointments_for_date(target_date):
    start_of_day = datetime.combine(target_date, time.min)
    end_of_day = datetime.combine(target_date, time.max)

    return Appointment.query.filter(
        Appointment.appointment_date >= start_of_day,
        Appointment.appointment_date <= end_of_day,
        Appointment.status == 'APPROVED'
    ).all()


def get_existing_notification(appointment_id, notif_type):
    return Notification.query.filter_by(
        appointment_id=appointment_id,
        type=notif_type
    ).first()


def get_doctor_user_info(doctor_profile_id):
    return User.query.join(DoctorProfile, User.id == DoctorProfile.user_id) \
        .filter(DoctorProfile.id == doctor_profile_id).first()


def get_patient_user_info(patient_profile_id):
    return User.query.join(PatientProfile, User.id == PatientProfile.user_id) \
        .filter(PatientProfile.id == patient_profile_id).first()


def insert_notifications_list(created_notifications, connection):
    notification_ids = []

    for data in created_notifications:
        stmt = Notification.__table__.insert().values(
            title=data['title'],
            message=data['message'],
            user_id=data['user_id'],
            appointment_id=data['appointment_id'],
            type=data['type'],
            is_read=data['is_read'],
            send_email=data['send_email'],
            email_status=data['email_status']
        )

        result = connection.execute(stmt)
        inserted_id = result.inserted_primary_key[0]
        notification_ids.append(inserted_id)

    return notification_ids


def get_pending_email_notifications():
    time_threshold = datetime.now() - timedelta(minutes=15)

    return Notification.query.filter(
        Notification.send_email == True,
        Notification.email_status == DeliveryStatus.PENDING,
        Notification.created_date <= time_threshold
    ).all()
