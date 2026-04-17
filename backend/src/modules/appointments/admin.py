from src.modules.appointments.models import Appointment, BookingLock
from src.modules.users.admin import AdminModelView


class AppointmentModelView(AdminModelView):
    column_searchable_list = ['name']
    column_filters = ['status', 'appointment_date']
    form_excluded_columns = ['created_date', 'updated_date', 'notifications', 'medical_record']


class BookingLockModelView(AdminModelView):
    column_searchable_list = ['doctor_name', 'service_name']
    column_filters = ['appointment_date', 'created_date']
    column_list = ['id', 'doctor_name', 'service_name', 'appointment_date', 'created_date']
    form_excluded_columns = ['created_date', 'updated_date']


def appointments(admin, db):
    admin.add_view(AppointmentModelView(Appointment, db.session, category="Quản lý lịch hẹn", name='Lịch hẹn'))
    admin.add_view(BookingLockModelView(BookingLock, db.session, category="Quản lý lịch hẹn", name='Khóa giữ chỗ'))
