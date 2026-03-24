from flask import redirect
from flask_admin import Admin, BaseView, expose
from flask_admin.theme import Bootstrap4Theme
from flask_login import logout_user

from src.modules.appointments.admin import appointments
from src.modules.auth_profile.admin import auth_profile
from src.modules.doctor.admin import doctor
from src.modules.medical_records.admin import medical_records
from src.modules.notification.admin import notification


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

admin = Admin(name="Clinic Admin", theme=Bootstrap4Theme())

def init_admin(app, db):
    admin.init_app(app)
    auth_profile(admin, db)
    doctor(admin, db)
    appointments(admin, db)
    medical_records(admin, db)
    notification(admin, db)
    admin.add_view(LogoutView(name='Đăng xuất'))
