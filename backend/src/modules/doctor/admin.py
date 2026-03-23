from flask_admin.contrib.sqla import ModelView
from src.modules.doctor.models import WorkSchedule, WorkDate

def doctor(admin, db):
    admin.add_view(ModelView(WorkSchedule, db.session))
    admin.add_view(ModelView(WorkDate, db.session))