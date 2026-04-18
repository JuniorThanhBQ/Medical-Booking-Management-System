import datetime

from flask import flash
from flask_admin.contrib.sqla import ModelView
from flask_admin.model import InlineFormAdmin
from flask_admin.model.typefmt import BASE_FORMATTERS
from werkzeug.security import generate_password_hash
from wtforms import FileField

from src.libs.cloudinary import cloudinary_upload_process
from src.modules.users.models import PatientProfile, Profile, User

account_profile_label = 'Tài khoản và hồ sơ'


def vn_datetime_formatter(_view, value):
    if value is None:
        return ""

    return value.strftime('%d/%m/%Y %H:%M:%S')


def vn_date_formatter(_view, value):
    if value is None:
        return ""
    return value.strftime('%d/%m/%Y')


CUSTOM_FORMATTERS = dict(BASE_FORMATTERS)

CUSTOM_FORMATTERS.update({
    datetime.datetime: vn_datetime_formatter,
    datetime.date: vn_date_formatter
})

ModelView.column_type_formatters = CUSTOM_FORMATTERS


class ProfileInline(InlineFormAdmin):
    form_excluded_columns = ['created_date', 'updated_date']
    form_choices = {
        'profile_type': [
            ('profile', 'Hồ sơ chung'),
            ('doctor', 'Bác sĩ'),
            ('patient', 'Bệnh nhân')
        ]
    }


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
    form_excluded_columns = AdminModelView.form_excluded_columns + ['avatar']
    form_choices = {
        'profile_type': [
            ('profile', 'Hồ sơ chung (Profile)'),
            ('doctor', 'Bác sĩ (Doctor)'),
            ('patient', 'Bệnh nhân (Patient)')
        ]
    }

    form_extra_fields = {
        'avatar_upload': FileField('Tải ảnh đại diện')
    }

    def on_model_change(self, form, model, is_created):
        file_data = form.avatar_upload.data
        if file_data:
            try:
                secure_url = cloudinary_upload_process(file_data)
                model.avatar = secure_url
            except Exception as e:
                flash(f'Lỗi khi tải ảnh lên Cloudinary: {str(e)}', 'error')
        return super().on_model_change(form, model, is_created)


class PatientProfileView(AdminModelView):
    form_excluded_columns = (AdminModelView.form_excluded_columns +
                             ['appointments', 'medical_records', 'avatar'])

    form_extra_fields = {
        'avatar_upload': FileField('Tải ảnh đại diện')
    }

    def on_model_change(self, form, model, is_created):
        file_data = form.avatar_upload.data
        if file_data:
            try:
                secure_url = cloudinary_upload_process(file_data)
                model.avatar = secure_url
            except Exception as e:
                flash(f'Lỗi khi tải ảnh lên Cloudinary: {str(e)}', 'error')
        return super().on_model_change(form, model, is_created)


def auth_profile(admin, db):
    admin.add_view(UserModelView(User, db.session, category=account_profile_label,
                                 name='Tài khoản User'))
    admin.add_view(ProfileModelView(Profile, db.session,
                                    category=account_profile_label, name='Hồ sơ chung'))
    admin.add_view(PatientProfileView(PatientProfile, db.session,
                                      category=account_profile_label, name='Hồ sơ bệnh nhân'))
