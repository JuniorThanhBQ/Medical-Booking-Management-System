from flask import Blueprint

from src.modules.appointments.routers import appointments_blueprint
from src.modules.auth_profile.routers import auth_profile_blueprint
from src.modules.doctor.routers import doctors_blueprint
from src.modules.medical_records.routers import medical_records_blueprint
from src.modules.public.routers import public_blueprint

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

api_v1.register_blueprint(auth_profile_blueprint, url_prefix="/auth")
api_v1.register_blueprint(public_blueprint, url_prefix="/public")
api_v1.register_blueprint(appointments_blueprint, url_prefix="/appointments")
api_v1.register_blueprint(medical_records_blueprint, url_prefix="")
api_v1.register_blueprint(doctors_blueprint, url_prefix="")
