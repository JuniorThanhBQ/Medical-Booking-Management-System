from sqlalchemy import event

from flask import current_app

from src.modules.notification.models import NotificationType, DeliveryStatus
from src.modules.appointments.models import Appointment
from src.modules.notification.repositories import (get_doctor_user_info,
                                                   get_patient_user_info,
                                                   insert_notifications_list)
from src.modules.notification.tasks import reminder_email_task


def insert_appointment_notifications(appointment, action_name):
    doctor = get_doctor_user_info(appointment.doctor_profile_id)
    patient = get_patient_user_info(appointment.patient_profile_id)

    if doctor and patient:
        doctor_name = f"{doctor.last_name} {doctor.first_name}"
        patient_name = f"{patient.last_name} {patient.first_name}"

        created_notifications = [
            {
                "title": f"Lịch hẹn {appointment.name} đã được {action_name}",
                "message": f"Chào {patient_name}, lịch hẹn của bạn với BS. {doctor_name} đã được {action_name}.",
                "user_id": patient.id,
                "appointment_id": appointment.id,
                "type": NotificationType["APPOINTMENT"],
                "is_read": False,
                "send_email": True,
                "email_status": DeliveryStatus["PENDING"]
            },
            {
                "title": f"Thông báo {action_name} trong lịch hẹn {appointment.name}",
                "message": f"Chào BS. {doctor_name}, lịch hẹn của bệnh nhân {patient_name} vừa được {action_name}.",
                "user_id": doctor.id,
                "appointment_id": appointment.id,
                "type": NotificationType["APPOINTMENT"],
                "is_read": False,
                "send_email": True,
                "email_status": DeliveryStatus["PENDING"]
            }
        ]

        notification_list = insert_notifications_list(created_notifications)

        for notification_id in notification_list:
            reminder_email_task.apply_async(args=[notification_id], countdown=5)


@event.listens_for(Appointment, 'after_insert')
def appointment_insert_listener(_mapper, connection, target):
    if current_app.config.get("DISABLE_SIGNALS"):
        return

    insert_appointment_notifications(target, action_name="chấp thuận")


@event.listens_for(Appointment, 'after_update')
def appointment_update_listener(_mapper, connection, target):
    if current_app.config.get("DISABLE_SIGNALS"):
        return

    insert_appointment_notifications(target, action_name="thay đổi")
