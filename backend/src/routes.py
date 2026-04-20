from flask import Blueprint
from flask_restx import Api

from src.modules.appointments.routers import appointments_namespace
from src.modules.doctors.routers import doctors_namespace, public_namespace
from src.modules.medical_records.routers import medical_records_namespace
from src.modules.notification.routers import notification_namespace
from src.modules.users.routers import auth_namespace

authorizations = {
    'api_key': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Bearer <token>"
    }
}

api_v2 = Blueprint("api_v2", __name__, url_prefix="/api/v2")
api = Api(
    api_v2,
    version='3.0.0',
    title='Medical Appointment B3 API',
    description='Tài liệu tổng hợp APIs trong hệ thống',
    authorizations=authorizations,
    doc='/docs'
)

api.add_namespace(auth_namespace, path="/auth")
api.add_namespace(public_namespace, path="/public")
api.add_namespace(appointments_namespace, path="/appointments")
api.add_namespace(medical_records_namespace, path="/medical-records")
api.add_namespace(doctors_namespace, path="/doctors")
api.add_namespace(notification_namespace, path="/notifications")
