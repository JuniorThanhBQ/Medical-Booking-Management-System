from flask import request
from flask_restful import Resource

from src.utils.decorator import token_required
from src.modules.doctor.services import (get_my_schedule_service,
                                         request_schedule_change_service)
from src.utils.utils import check_xss_violation, format_api_response


class RetrieveMyScheduleAPI(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        return format_api_response(
            *get_my_schedule_service(current_user)
        )


class ScheduleRequestAPI(Resource):
    method_decorators = [token_required]

    def post(self, current_user):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation([data.get("reason", "")]):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *request_schedule_change_service(current_user, data), success_code=201
        )
