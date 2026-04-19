import logging

from flask import render_template
from flask_mail import Message

from src.extensions import celery_app, mail

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def send_verification_email_task(self, user_email, verification_link):
    try:
        message = Message(
            subject="Xác thực tài khoản - Medical Appointment B3",
            recipients=[user_email],
        )

        message.html = render_template(
            'emails/email_verification.html',
            verification_link=verification_link
        )

        mail.send(message)
        logger.info(f"Đã gửi email xác thực thành công tới {user_email}")

    except Exception as e:
        logger.error(f"Lỗi gửi email xác thực tới {user_email}: {str(e)}")
        raise self.retry(exc=e, countdown=60)
