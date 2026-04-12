from src.modules.notification.models import Notification
from src.modules.users.admin import AdminModelView


class NotificationModelView(AdminModelView):
    column_list = ['id', 'user', 'title', 'type', 'is_read', 'send_email', 'email_status', 'appointment']
    column_searchable_list = ['title', 'user.email', 'user.username']
    column_filters = ['is_read', 'type', 'send_email', 'email_status', 'user.email']


def notification(admin, db):
    admin.add_view(NotificationModelView(Notification, db.session, name='Thông báo'))
