from src.modules.appointments.models import Appointment, MedicalRecord
from src.modules.users.admin import AdminModelView


class AppointmentModelView(AdminModelView):
    column_searchable_list = ['name']
    column_filters = ['status', 'appointment_date']
    form_excluded_columns = ['created_date', 'updated_date', 'notifications', 'medical_record']


def appointments(admin, db):
    admin.add_view(AppointmentModelView(Appointment, db.session, name='Lịch hẹn'))


class MedicalRecordModelView(AdminModelView):
    column_searchable_list = ['diagnosis']
    column_filters = ['type']
    form_excluded_columns = ['created_date', 'updated_date', 'appointment']


def medical_records(admin, db):
    admin.add_view(MedicalRecordModelView(MedicalRecord, db.session, name='Phiếu điều trị'))
