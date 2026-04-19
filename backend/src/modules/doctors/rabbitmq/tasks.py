import logging
import os

from flask import render_template
from flask_mail import Message

from src.extensions import celery_app, mail

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def process_doctor_registration_email(self, data, file_path, filename):
    try:
        hr_email = "thanh.vantrung2005@gmail.com"

        msg = Message(
            subject=f"Hồ sơ ứng tuyển Bác sĩ mới: {data.get('fullName', 'Ứng viên')}",
            recipients=[hr_email]
        )

        msg.html = render_template('emails/doctors_registration.html', data=data)

        if os.path.exists(file_path):
            try:
                with open(file_path, 'rb') as fp:
                    msg.attach(filename, 'application/pdf', fp.read())
            except FileNotFoundError as e:
                logger.error(f"Không tìm thấy file CV tại Worker: {file_path}")
                raise self.retry(exc=e, countdown=60)

        mail.send(msg)

    except Exception as e:
        logger.error(f"Lỗi gửi email ứng tuyển bác sĩ: {e}")
        raise self.retry(exc=e, countdown=60)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
