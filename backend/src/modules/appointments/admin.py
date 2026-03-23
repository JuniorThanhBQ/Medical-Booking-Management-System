from flask_admin.contrib.sqla import ModelView
from src.modules.appointments.models import Appointment

def appointments(admin, db):
    admin.add_view(ModelView(Appointment, db.session, category='appointment'))
