from flask_admin.contrib.sqla import ModelView
from src.modules.auth_profile.models import User, Profile, Specialty, DoctorProfile, PatientProfile, AuditLog

def auth_profile(admin, db):
    admin.add_view(ModelView(User, db.session, category='auth_profile'))
    admin.add_view(ModelView(Profile, db.session, category='auth_profile'))
    admin.add_view(ModelView(DoctorProfile, db.session, category='auth_profile'))
    admin.add_view(ModelView(PatientProfile, db.session, category='auth_profile'))
    admin.add_view(ModelView(Specialty, db.session, category='appointment'))
    admin.add_view(ModelView(AuditLog, db.session))