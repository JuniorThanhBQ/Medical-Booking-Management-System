from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin
from werkzeug.security import generate_password_hash

from src.modules.auth_profiles.models import (AuditLog, DoctorProfile,
                                              PatientProfile, Profile,
                                              Specialty, User)


class ProfileInline(InlineFormAdmin):
    form_excluded_columns = ['created_date', 'updated_date']
    form_choices = {
        'profile_type': [
            ('profile', 'Hồ sơ chung (Profile)'),
            ('doctor', 'Bác sĩ (Doctor)'),
            ('patient', 'Bệnh nhân (Patient)')
        ]
    }


class DoctorProfileInline(InlineFormAdmin):
    form_excluded_columns = ['created_date', 'updated_date', 'appointments',
                             'medical_records', 'work_schedule']


class PatientProfileInline(InlineFormAdmin):
    form_excluded_columns = ['created_date', 'updated_date', 'appointments',
                             'medical_records']


class AdminModelView(ModelView):
    form_excluded_columns = ['created_date', 'updated_date']


class UserModelView(AdminModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['username', 'email', 'first_name', 'last_name']
    column_filters = ['role', 'is_active']
    form_excluded_columns = (AdminModelView.form_excluded_columns +
                             ['profile', 'audit_log', 'notifications'])

    inline_models = [ProfileInline(Profile)]

    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.password = generate_password_hash(form.password.data)
        return super().on_model_change(form, model, is_created)


class ProfileModelView(AdminModelView):
    form_choices = {
        'profile_type': [
            ('profile', 'Hồ sơ chung (Profile)'),
            ('doctor', 'Bác sĩ (Doctor)'),
            ('patient', 'Bệnh nhân (Patient)')
        ]
    }


class DoctorProfileView(AdminModelView):
    form_excluded_columns = (AdminModelView.form_excluded_columns +
                             ['appointments', 'medical_records', 'work_schedule'])


class PatientProfileView(AdminModelView):
    form_excluded_columns = (AdminModelView.form_excluded_columns +
                             ['appointments', 'medical_records'])


def auth_profile(admin, db):
    account_profile_label = 'Tài khoản và hồ sơ'
    admin.add_view(UserModelView(User, db.session, category=account_profile_label,
                                 name='Tài khoản User'))
    admin.add_view(ProfileModelView(Profile, db.session,
                                    category=account_profile_label, name='Hồ sơ chung'))
    admin.add_view(DoctorProfileView(DoctorProfile, db.session,
                                     category=account_profile_label, name='Hồ sơ Bác sĩ'))
    admin.add_view(PatientProfileView(PatientProfile, db.session,
                                      category=account_profile_label, name='Hồ sơ Bệnh nhân'))
    admin.add_view(AdminModelView(Specialty, db.session,
                                  name='Chuyên khoa'))
    admin.add_view(AdminModelView(AuditLog, db.session,
                                  name='Lịch sử hệ thống'))
