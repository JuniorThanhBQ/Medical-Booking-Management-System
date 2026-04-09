import logging
from datetime import datetime, timedelta

from flask import render_template
from flask_mail import Message

from src.extensions import celery_app, mail
from src.modules.notification.models import (DeliveryStatus, Notification,
                                             NotificationType)
from src.modules.notification.repositories import (add_and_commit_notification,
                                                   get_existing_notification,
                                                   get_notification_by_id,
                                                   get_upcoming_appointments,
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
        logger.error(f"Lỗi gửi email cho thông báo mã {notification_id}: ")
        if self.request.retries >= self.max_retries:
            update_email_status(notification, DeliveryStatus.FAILED)

        raise self.retry(exc=e, countdown=60)


@celery_app.task
def reminders_task_schedule():
    now = datetime.now()
    target_time_start = now + timedelta(hours=23)
    target_time_end = now + timedelta(hours=25)
    upcoming_appointments = get_upcoming_appointments(target_time_start, target_time_end)

    for appointment in upcoming_appointments:
        existing_notification = get_existing_notification(
            appointment_id=appointment.id,
            notif_type=NotificationType.APPOINTMENT
        )

        if not existing_notification:
            new_notification = Notification(
                title="Nhắc nhở lịch khám bệnh",
                message=f"Xin chào {appointment.user.username}, bạn có lịch vào lúc {appointment.appointment_date}.",
                type=NotificationType.APPOINTMENT,
                send_email=True,
                email_status=DeliveryStatus.PENDING,
                user_id=appointment.user_id,
                appointment_id=appointment.id
            )

            add_and_commit_notification(new_notification)
            reminder_email_task.delay(new_notification.id)

            logger.info(f"Đã tạo và lên lịch nhắc hẹn cho {appointment.name}")
