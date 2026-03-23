from flask_admin import Admin
from flask_admin.theme import Bootstrap4Theme
from src.modules.auth_profile.admin import auth_profile
from src.modules.doctor.admin import doctor
from src.modules.appointments.admin import appointments
from src.modules.medical_records.admin import medical_records
from src.modules.notification.admin import notification

admin = Admin(name="Clinic", theme=Bootstrap4Theme())

def init_admin(app, db):
    admin.init_app(app)

    auth_profile(admin, db)
    doctor(admin, db)
    appointments(admin, db)
    medical_records(admin, db)
    notification(admin, db)