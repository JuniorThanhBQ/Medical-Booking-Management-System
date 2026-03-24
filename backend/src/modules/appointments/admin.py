from src.modules.appointments.models import Appointment
from src.modules.auth_profile.admin import AdminModelView


class AppointmentModelView(AdminModelView):
    column_searchable_list = ['name']
    column_filters = ['status', 'appointment_date']
    form_excluded_columns = ['created_date', 'updated_date', 'notifications', 'medical_record']

def appointments(admin, db):
    admin.add_view(AppointmentModelView(Appointment, db.session, name='Lịch hẹn'))
