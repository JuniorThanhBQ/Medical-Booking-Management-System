import random
from functools import partial

from flask import current_app
from sqlalchemy import event

from src.extensions import db
from src.modules.appointments.models import Appointment
from src.modules.notification.rabbitmq.tasks import reminder_email_task
from src.modules.notification.services import insert_appointment_notifications


def hook_after_commit(_session, notification_list):
    for notification_id in notification_list:
        jitter = random.randint(1, 10)
        reminder_email_task.apply_async(
            args=[notification_id],
            countdown=jitter
        )


def processing_appointment_notification(target, connection=None, action_name=None):
    if current_app.config.get("DISABLE_SIGNALS") or connection is None:
        return

    notification_list = insert_appointment_notifications(appointment=target, connection=connection,
                                                         action_name=action_name)

    if not notification_list:
        return

    callback = partial(hook_after_commit, notification_list=notification_list)
    event.listen(db.session, 'after_commit', callback, once=True)


@event.listens_for(Appointment, 'after_insert')
def appointment_insert_listener(_mapper, connection, target):
    processing_appointment_notification(target, connection=connection, action_name="tạo như sau")


@event.listens_for(Appointment, 'after_update')
def appointment_update_listener(_mapper, connection, target):
    processing_appointment_notification(target, connection=connection, action_name="cập nhật như sau")
