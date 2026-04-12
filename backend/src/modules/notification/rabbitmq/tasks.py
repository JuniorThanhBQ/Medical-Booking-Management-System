import logging
from datetime import datetime, timedelta

from flask import render_template
from flask_mail import Message

from src.extensions import celery_app, mail
from src.modules.notification.models import (DeliveryStatus, Notification,
                                             NotificationType)
from src.modules.notification.repositories import (
    add_and_commit_notification, get_appointments_for_date,
    get_doctor_user_info, get_existing_notification, get_notification_by_id,
    get_patient_user_info, get_pending_email_notifications,
    update_email_status)

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=5)
def reminder_email_task(self, notification_id):
    notification = get_notification_by_id(notification_id=notification_id)

    if not notification or notification.email_status != DeliveryStatus.PENDING:
        return

    try:
        user_email = notification.user.email
        message = Message(
            subject=notification.title,
            recipients=[user_email],
        )
        message.body = notification.message
        message.html = render_template('emails/notification.html', notification=notification)

        mail.send(message)
        update_email_status(notification, DeliveryStatus.SENT)

    except Exception as e:
        logger.error(f"Lỗi gửi email cho thông báo {notification_id}: ")
        if self.request.retries >= self.max_retries:
            update_email_status(notification, DeliveryStatus.FAILED)

        raise self.retry(exc=e, countdown=60)


@celery_app.task
def reminders_task_schedule():
    tomorrow = datetime.now().date() + timedelta(days=1)
    upcoming_appointments = get_appointments_for_date(tomorrow)

    if not upcoming_appointments:
        logger.info(f"Không có lịch hẹn cho ({tomorrow}).")
        return

    count = 0
    for appointment in upcoming_appointments:
        existing_notification = get_existing_notification(
            appointment_id=appointment.id,
            notif_type=NotificationType.REMINDER
        )

        if not existing_notification:
            appointment_time = appointment.appointment_date.strftime("%H:%M")
            date_str = tomorrow.strftime('%d/%m/%Y')

            doctor = get_doctor_user_info(appointment.doctor_profile_id)
            patient = get_patient_user_info(appointment.patient_profile_id)

            notifications_to_add = []

            if patient:
                patient_name = f"{patient.last_name} {patient.first_name}"
                doctor_name = f"{doctor.last_name} {doctor.first_name}" if doctor else "Bác sĩ"

                patient_notification = Notification(
                    title="Nhắc nhở: Lịch hẹn khám bệnh ngày mai",
                    message=(f"Xin chào {patient_name}, "
                             f"bạn có lịch khám với BS. {doctor_name} vào lúc {appointment_time} "
                             f"ngày mai ({date_str}) tại 97 Võ Văn Tần. "
                             f"Chúc bạn có một ngày tốt lành."),
                    type=NotificationType.REMINDER,
                    send_email=True,
                    email_status=DeliveryStatus.PENDING,
                    user_id=patient.id,
                    appointment_id=appointment.id
                )
                notifications_to_add.append(patient_notification)

            if doctor:
                patient_name = f"{patient.last_name} {patient.first_name}" if patient else "Khách hàng"

                doctor_notification = Notification(
                    title="Nhắc nhở: Lịch làm việc ngày mai",
                    message=(f"Xin chào BS. {doctor.last_name} {doctor.first_name}, "
                             f"Bác sĩ có lịch khám cho bệnh nhân {patient_name} "
                             f"vào lúc {appointment_time} ngày mai ({date_str}). "
                             f"Chúc bác sĩ một ngày làm việc hiệu quả."),
                    type=NotificationType.REMINDER,
                    send_email=True,
                    email_status=DeliveryStatus.PENDING,
                    user_id=doctor.id,
                    appointment_id=appointment.id
                )
                notifications_to_add.append(doctor_notification)

            for notification in notifications_to_add:
                add_and_commit_notification(notification)
                reminder_email_task.delay(notification.id)
                count += 1

    logger.info(f"Tổng cộng: {count} thông báo nhắc lịch trong ngày.")


@celery_app.task
def pending_emails_task_schedule():
    pending_notifications = get_pending_email_notifications()

    if not pending_notifications:
        logger.info("Không có email cần gửi.")
        return

    logger.info(f"Tìm thấy {len(pending_notifications)} email đang chờ gửi.")

    for notification in pending_notifications:
        reminder_email_task.delay(notification.id)
