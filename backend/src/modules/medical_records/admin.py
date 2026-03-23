from flask_admin.contrib.sqla import ModelView
from src.modules.medical_records.models import MedicalRecord

def medical_records(admin, db):
    admin.add_view(ModelView(MedicalRecord, db.session, category='appointment'))
