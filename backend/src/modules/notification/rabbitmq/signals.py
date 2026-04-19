import secrets
from functools import partial

from dependency_injector.wiring import Provide, inject
from flask import current_app
from sqlalchemy import event

from src.containers import AppContainer
from src.extensions import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.notification.rabbitmq.tasks import reminder_email_task


def hook_after_commit(_session, notification_list):
    for notification_id in notification_list:
        jitter = secrets.SystemRandom().randint(1, 10)
        reminder_email_task.apply_async(
            args=[notification_id],
            countdown=jitter
        )


@inject
def processing_appointment_notification(appointment=None, connection=None, action_name=None,
                                        notification_services=Provide[
                                            AppContainer.notification_app.notification_services
                                        ]):
    if (current_app.config.get("DISABLE_SIGNALS")
            or connection is None or appointment is None):
        return

    if appointment.status == StatusRole.COMPLETED:
        return

    notification_list = notification_services.insert_appointment_notifications(
        appointment=appointment, connection=connection, action_name=action_name)

    if not notification_list:
        return

    callback = partial(hook_after_commit, notification_list=notification_list)
    event.listen(db.session, 'after_commit', callback, once=True)


@event.listens_for(Appointment, 'after_insert')
def appointment_insert_listener(_mapper, connection, target):
    processing_appointment_notification(appointment=target, connection=connection, action_name="tạo như sau")


@event.listens_for(Appointment, 'after_update')
def appointment_update_listener(_mapper, connection, target):
    processing_appointment_notification(appointment=target, connection=connection, action_name="thay đổi")
