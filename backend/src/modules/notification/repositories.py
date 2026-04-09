from sqlalchemy import desc

from flask import current_app

from src.extensions import db
from src.modules.appointments.models import Appointment
from src.modules.doctors.models import DoctorProfile
from src.modules.notification.models import Notification
from src.modules.users.models import PatientProfile, User


def get_paginated_by_user_id(user_id, page=1, per_page=10):
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


def get_upcoming_appointments(target_time_start, target_time_end):
    return Appointment.query.filter(
        Appointment.appointment_date >= target_time_start,
        Appointment.appointment_date <= target_time_end,
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


def insert_notifications_list(created_notifications):
    notifications = []

    for data in created_notifications:
        notification = Notification()
        notification.title = data['title']
        notification.message = data['message']
        notification.user_id = data['user_id']
        notification.appointment_id = data['appointment_id']
        notification.type = data['type']
        notification.is_read = data['is_read']
        notification.send_email = data['send_email']
        notification.email_status = data['email_status']
        db.session.add(notification)
        notifications.append(notification)

    db.session.commit()
    return [n.id for n in notifications]

