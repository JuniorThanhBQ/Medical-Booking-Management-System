from src.modules.notification.repositories import (bulk_mark_as_read, commit,
                                                   delete_notification,
                                                   get_by_id_and_user_id,
                                                   get_paginated_by_user_id,
                                                   get_unread_by_user_id)


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
