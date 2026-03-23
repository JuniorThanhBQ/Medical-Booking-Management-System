from flask import request
from flask_restful import Resource

from src.modules.medical_records.services import (
    create_medical_record_service, get_detail_medical_record_service,
    update_medical_record_service)
from src.utils.decorator import token_required
from src.utils.utils import check_xss_violation, format_api_response


class MedicalRecordRetrieveUpdateAPI(Resource):
    method_decorators = [token_required]

    def get(self, current_user, medical_record_id):
        return format_api_response(
            *get_detail_medical_record_service(current_user, medical_record_id)
        )

    def patch(self, current_user, medical_record_id):
        data = request.get_json(silent=True) or request.form.to_dict()
        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *update_medical_record_service(current_user, medical_record_id, data))


class CreateMedicalRecordAPI(Resource):
    method_decorators = [token_required]

    def post(self, current_user, appointment_id):
        data = request.get_json(silent=True) or request.form.to_dict()

        if not data:
            return {"message": "Dữ liệu gửi lên không được để trống"}, 400

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *create_medical_record_service(current_user, appointment_id, data),
            success_code=201
        )
