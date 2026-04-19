import logging

from dependency_injector.wiring import Provide, inject
from flask import current_app, render_template
from flask_mail import Message

from src.containers import AppContainer
from src.extensions import celery_app, mail
from src.modules.notification.models import DeliveryStatus

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=5)
@inject
def reminder_email_task(
        self,
        notification_id,
        notification_repository=Provide[AppContainer.notification_app.repository]
):
    notification = notification_repository.get_notification_by_id(notification_id=notification_id)

    if not notification or notification.email_status != DeliveryStatus.PENDING:
        return

    try:
        user_email = notification.user.email
        message = Message(
            subject=notification.title,
            recipients=[user_email],
        )
        message.body = notification.message
        message.html = render_template(
            'emails/notification.html',
            notification=notification,
            app_url=current_app.config.get("FRONTEND_URL")
        )

        mail.send(message)
        notification_repository.update_email_status(notification, DeliveryStatus.SENT)

    except Exception as e:
        logger.error(f"Lỗi gửi email cho thông báo {notification_id}: {str(e)}")
        if self.request.retries >= self.max_retries:
            notification_repository.update_email_status(notification, DeliveryStatus.FAILED)

        raise self.retry(exc=e, countdown=60)


@celery_app.task
@inject
def reminders_task_schedule(
        notification_services=Provide[AppContainer.notification_app.mail_services]
):
    notification_ids = notification_services.generate_daily_reminders_service()

    for notif_id in notification_ids:
        reminder_email_task.delay(notif_id)


@celery_app.task
@inject
def pending_emails_task_schedule(
        notification_services=Provide[AppContainer.notification_app.mail_services]
):
    pending_ids = notification_services.get_pending_emails_service()

    if not pending_ids:
        logger.info("Không có email cần gửi.")
        return

    logger.info(f"Tìm thấy {len(pending_ids)} email đang chờ gửi.")
    for notif_id in pending_ids:
        reminder_email_task.delay(notif_id)
