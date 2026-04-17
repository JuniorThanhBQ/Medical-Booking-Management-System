from src.modules.doctors.models import (DoctorProfile, MedicalService,
                                        Specialty, VisitType, WorkDate,
                                        WorkSchedule)
from src.modules.users.admin import AdminModelView, account_profile_label


class WorkScheduleModelView(AdminModelView):
    column_searchable_list = ['title']
    form_excluded_columns = ['created_date', 'updated_date']
    inline_models = [(WorkDate, {'form_excluded_columns': ['created_date', 'updated_date']})]


class DoctorProfileView(AdminModelView):
    form_excluded_columns = (AdminModelView.form_excluded_columns +
                             ['appointments', 'medical_records', 'work_schedule'])


class SpecialtyModelView(AdminModelView):
    form_excluded_columns = ['created_date', 'updated_date']
    inline_models = [(MedicalService, {'form_excluded_columns': ['created_date', 'updated_date']})]


class MedicalServiceModelView(AdminModelView):
    form_excluded_columns = ['created_date', 'updated_date']


def doctor(admin, db):
    admin.add_view(WorkScheduleModelView(WorkSchedule, db.session,
                                         category='Lịch làm việc', name='Lịch trình'))
    admin.add_view(DoctorProfileView(DoctorProfile, db.session,
                                     category=account_profile_label, name='Hồ sơ Bác sĩ'))
    admin.add_view(SpecialtyModelView(Specialty, db.session,
                                      category='Chuyên khoa và dịch vụ', name='Chuyên khoa'))
    admin.add_view(MedicalServiceModelView(MedicalService, db.session,
                                           category='Chuyên khoa và dịch vụ', name='Dịch vụ y tế'))
    admin.add_view(AdminModelView(VisitType, db.session,
                                  category='Chuyên khoa và dịch vụ', name='Loại khám'))
