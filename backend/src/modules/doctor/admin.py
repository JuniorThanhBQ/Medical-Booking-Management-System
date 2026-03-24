from src.modules.auth_profile.admin import AdminModelView
from src.modules.doctor.models import WorkDate, WorkSchedule


class WorkScheduleModelView(AdminModelView):
    column_searchable_list = ['title']
    form_excluded_columns = ['created_date', 'updated_date']
    inline_models = [(WorkDate, {'form_excluded_columns': ['created_date', 'updated_date']})]

def doctor(admin, db):
    admin.add_view(WorkScheduleModelView(WorkSchedule, db.session,
                                         category='Lịch làm việc', name='Lịch trình (Kèm ngày)'))
