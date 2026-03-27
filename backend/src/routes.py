from flask import Blueprint
from flask_restx import Api

from src.modules.appointments.routers import appointments_namespace
from src.modules.auth_profiles.routers import auth_namespace
from src.modules.doctors.routers import doctors_namespace
from src.modules.medical_records.routers import medical_records_namespace
from src.modules.notification.routers import notification_namespace
from src.modules.public.routers import public_namespace

api_v1 = Blueprint("api_v1", __name__, url_prefix="/api/v1")

authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Công thức là Bearer <your_token>"
    }
}

api = Api(
    api_v1,
    version='3.0.0',
    title='Medical Appointment B3 API',
    description='Tài liệu tổng hợp tất cả các phân hệ',
    authorizations=authorizations,
    doc='/docs'
)

api.add_namespace(auth_namespace, path="/auth")
api.add_namespace(public_namespace, path="/public")
api.add_namespace(appointments_namespace, path="/appointments")
api.add_namespace(medical_records_namespace, path="/medical-records")
api.add_namespace(doctors_namespace, path="/doctors")
api.add_namespace(notification_namespace, path="/notifications")
