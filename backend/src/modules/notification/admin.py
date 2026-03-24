from src.modules.auth_profile.admin import AdminModelView
from src.modules.notification.models import Notification


class NotificationModelView(AdminModelView):
    column_searchable_list = ['title']
    column_filters = ['is_read']

def notification(admin, db):
    admin.add_view(NotificationModelView(Notification, db.session, name='Thông báo'))
