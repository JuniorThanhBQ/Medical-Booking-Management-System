from flask import redirect, request, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from flask_admin.theme import Bootstrap4Theme
from flask_login import current_user

from src.modules.appointments.admin import appointments
from src.modules.auth_profiles.admin import auth_profile
from src.modules.doctors.admin import doctor
from src.modules.medical_records.admin import medical_records
from src.modules.notification.admin import notification


class MyAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.name == 'ADMIN'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_view', next=request.url))


class MyModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.name == 'ADMIN'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login_view', next=request.url))


admin = Admin(name="Medical Appointment B3", theme=Bootstrap4Theme(), index_view=MyAdminIndexView())


def init_admin(app, db):
    admin.init_app(app)
    auth_profile(admin, db)
    doctor(admin, db)
    appointments(admin, db)
    medical_records(admin, db)
    notification(admin, db)
    admin.add_link(MenuLink(name='Logout', endpoint='logout_view'))
