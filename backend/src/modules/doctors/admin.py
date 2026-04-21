from flask import flash
from wtforms import FileField

from src.libs.cloudinary import cloudinary_upload_process
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
    form_excluded_columns = ['created_date', 'updated_date', 'images']
    inline_models = [(MedicalService, {'form_excluded_columns': ['created_date', 'updated_date']})]

    form_extra_fields = {
        'image_upload': FileField('Tải ảnh lên')
    }

    def on_model_change(self, form, model, is_created):
        file_data = form.image_upload.data

        if file_data:
            try:
                secure_url = cloudinary_upload_process(file_data)
                model.images = secure_url
            except Exception as e:
                flash(f'Lỗi khi tải ảnh lên Cloudinary: {str(e)}', 'error')

        return super().on_model_change(form, model, is_created)


class MedicalServiceModelView(AdminModelView):
    form_excluded_columns = ['created_date', 'updated_date', 'appointments']


def doctor(admin, db):
    admin.add_view(WorkScheduleModelView(WorkSchedule, db.session,
                                         category='Lịch làm việc', name='Lịch công việc'))
    admin.add_view(DoctorProfileView(DoctorProfile, db.session,
                                     category=account_profile_label, name='Hồ sơ bác sĩ'))
    admin.add_view(SpecialtyModelView(Specialty, db.session,
                                      category='Chuyên khoa và dịch vụ', name='Chuyên khoa'))
    admin.add_view(MedicalServiceModelView(MedicalService, db.session,
                                           category='Chuyên khoa và dịch vụ', name='Dịch vụ y tế'))
    admin.add_view(AdminModelView(VisitType, db.session,
                                  category='Chuyên khoa và dịch vụ', name='Loại khám'))
