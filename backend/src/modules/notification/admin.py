from flask_admin.contrib.sqla import ModelView
from src.modules.notification.models import Notification

def notification(admin, db):
    admin.add_view(ModelView(Notification, db.session))
