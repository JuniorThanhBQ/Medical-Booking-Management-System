from src.modules.notification.models import DeliveryStatus, NotificationType
from src.modules.notification.repositories import (bulk_mark_as_read, commit,
                                                   delete_notification,
                                                   get_by_id_and_user_id,
                                                   get_doctor_user_info,
                                                   get_paginated_by_user_id,
                                                   get_patient_user_info,
                                                   get_unread_by_user_id,
                                                   insert_notifications_list,
                                                   rollback)


def get_notifications_service(current_user, page=1, per_page=10):
    paginated_data = get_paginated_by_user_id(current_user.id, page, per_page)

    data = {
        "items": [
            {
                "id": n.id,
                "title": n.title,
                "message": n.message,
                "is_read": n.is_read,
                "type": n.type.name if n.type else "SYSTEM",
                "created_at": n.created_date.isoformat() + "Z" if n.created_date else None,
            } for n in paginated_data.items
        ],
        "meta": {
            "page": paginated_data.page,
            "per_page": paginated_data.per_page,
            "total_pages": paginated_data.pages,
            "total_items": paginated_data.total,
            "has_next": paginated_data.has_next,
            "has_prev": paginated_data.has_prev
        }
    }

    return data, "SUCCESS"


def get_detail_notification_service(current_user, notification_id):
    notification = get_by_id_and_user_id(notification_id, current_user.id)
    if not notification:
        return None, "NOT_FOUND"

    result = {
        "id": notification.id,
        "title": notification.title,
        "message": notification.message,
        "is_read": notification.is_read,
        "type": notification.type.name if notification.type else "SYSTEM",
        "created_at": notification.created_date.isoformat() + "Z" if notification.created_date else None,
    }
    return result, "SUCCESS"


def mark_all_notification_service(current_user):
    unread_notifies = get_unread_by_user_id(current_user.id)
    if unread_notifies:
        bulk_mark_as_read(unread_notifies)
    return "", "SUCCESS"


def mark_detail_notification_service(current_user, notification_id):
    notification = get_by_id_and_user_id(notification_id, current_user.id)
    if not notification:
        return None, "NOT_FOUND"

    if not notification.is_read:
        notification.is_read = True
        commit()

    return "", "SUCCESS"


def delete_notification_service(current_user, notification_id):
    notification = get_by_id_and_user_id(notification_id, current_user.id)
    if not notification:
        return None, "NOT_FOUND"

    delete_notification(notification)
    return "", "SUCCESS"


def insert_appointment_notifications(appointment=None, connection=None, action_name=None):
    doctor = get_doctor_user_info(appointment.doctor_profile_id)
    patient = get_patient_user_info(appointment.patient_profile_id)

    if doctor and patient and connection is not None:
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
                "message": f"Chào BS. {doctor_name}, lịch hẹn của bệnh nhân {patient_name} "
                           f"do bạn phụ trách vừa được {action_name}.",
                "user_id": doctor.id,
                "appointment_id": appointment.id,
                "type": NotificationType["APPOINTMENT"],
                "is_read": False,
                "send_email": True,
                "email_status": DeliveryStatus["PENDING"]
            }
        ]

        try:
            notification_list = insert_notifications_list(created_notifications, connection)
            return notification_list
        except Exception as e:
            rollback()
            raise e

    return None
