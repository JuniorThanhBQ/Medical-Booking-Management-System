from src.modules.medical_records.models import MedicalRecord
from src.modules.users.admin import AdminModelView


class MedicalRecordModelView(AdminModelView):
    can_export = True
    column_searchable_list = ['diagnosis']
    column_filters = ['type']
    form_excluded_columns = ['created_date', 'updated_date']


def medical_records(admin, db):
    admin.add_view(MedicalRecordModelView(MedicalRecord, db.session, name='Phiếu điều trị'))
