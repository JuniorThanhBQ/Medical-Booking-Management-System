from flask import Blueprint
from flask_restful import Api

from src.modules.medical_records.views import (CreateMedicalRecordAPI,
                                               MedicalRecordRetrieveUpdateAPI)

medical_records_blueprint = Blueprint("medical_records", __name__)
api = Api(medical_records_blueprint)

api.add_resource(MedicalRecordRetrieveUpdateAPI, "/medical-records/<int:medical_record_id>")
api.add_resource(CreateMedicalRecordAPI, "/appointments/<int:appointment_id>/medical-record")
