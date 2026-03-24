from src.modules.auth_profile.admin import AdminModelView
from src.modules.medical_records.models import MedicalRecord


class MedicalRecordModelView(AdminModelView):
    column_searchable_list = ['diagnosis']
    column_filters = ['type']
    form_excluded_columns = ['created_date', 'updated_date', 'appointment']

def medical_records(admin, db):
    admin.add_view(MedicalRecordModelView(MedicalRecord, db.session, name='Phiếu điều trị'))
