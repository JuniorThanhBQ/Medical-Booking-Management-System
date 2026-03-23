from flask import request
from flask_restful import Resource

from src.modules.receptionist.services import \
    create_receptionist_appointment_service
from src.utils.decorator import token_required
from src.utils.utils import check_xss_violation, format_api_response


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
