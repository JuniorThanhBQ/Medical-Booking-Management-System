from src.modules.doctors.models import (DoctorProfile, Specialty, WorkDate,
                                        WorkSchedule)
from src.modules.users.admin import AdminModelView, account_profile_label


class WorkScheduleModelView(AdminModelView):
    column_searchable_list = ['title']
    form_excluded_columns = ['created_date', 'updated_date']
    inline_models = [(WorkDate, {'form_excluded_columns': ['created_date', 'updated_date']})]


class DoctorProfileView(AdminModelView):
    form_excluded_columns = (AdminModelView.form_excluded_columns +
                             ['appointments', 'medical_records', 'work_schedule'])


def doctor(admin, db):
    admin.add_view(WorkScheduleModelView(WorkSchedule, db.session,
                                         category='Lịch làm việc', name='Lịch trình (Kèm ngày)'))
    admin.add_view(DoctorProfileView(DoctorProfile, db.session,
                                     category=account_profile_label, name='Hồ sơ Bác sĩ'))
    admin.add_view(AdminModelView(Specialty, db.session,
                                  name='Chuyên khoa'))
