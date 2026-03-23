from flask import request
from flask_restful import Resource

from src.utils.utils import check_xss_violation, format_api_response

from src.utils.decorator import token_required
from .services import (create_patient_appointment_service,
                       create_receptionist_appointment_service,
                       delete_appointment_service,
                       get_appointment_detail_service,
                       get_appointments_list_service,
                       get_patient_profile_service,
                       patch_appointment_service)


class AppointmentListCreateAPI(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        return format_api_response(
            *get_appointments_list_service(current_user)
        )

    def post(self, current_user):
        data = request.get_json(silent=True) or request.form.to_dict()
        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *create_patient_appointment_service(current_user, data),
            success_code=201
        )


class AppointmentRetrieveUpdateAPI(Resource):
    method_decorators = [token_required]

    def get(self, current_user, appointment_id):
        return format_api_response(
            *get_appointment_detail_service(current_user, appointment_id)
        )

    def patch(self, current_user, appointment_id):
        data = request.get_json(silent=True) or request.form.to_dict()
        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *patch_appointment_service(current_user, appointment_id, data),
            success_code=204
        )

    def delete(self, current_user, appointment_id):
        return format_api_response(
            *delete_appointment_service(current_user, appointment_id),
            success_code=204
        )


class PatientRetrieveAPI(Resource):
    method_decorators = [token_required]

    def get(self, current_user, appointment_id):
        return format_api_response(
            *get_patient_profile_service(current_user, appointment_id)
        )


class ReceptionistAppointmentCreateAPI(Resource):
    method_decorators = [token_required]

    def post(self, current_user):
        data = request.get_json(silent=True) or request.form.to_dict()
        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *create_receptionist_appointment_service(current_user, data),
            success_code=201
        )
