from src.extensions import db

from .models import Notification


def get_notifications_service(current_user):
    notifications = (Notification.query.filter_by(user_id=current_user.id)
                     .order_by(Notification.created_date.desc()).all())

    result = [
        {
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "is_read": notification.is_read,
            "created_at":
                notification.created_date.isoformat() + "Z" if notification.created_date else None,
        } for notification in notifications
    ]

    return result, "SUCCESS"


def mark_notification_read_service(current_user):
    unread_notifies = Notification.query.filter_by(user_id=current_user.id, is_read=False).all()

    for notification in unread_notifies:
        notification.is_read = True

    db.session.commit()
    return "", "SUCCESS"
