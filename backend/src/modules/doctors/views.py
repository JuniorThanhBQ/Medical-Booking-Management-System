from flask import request
from flask_restx import Namespace, Resource, fields

from src.middlewares.auth import token_required
from src.modules.doctors.services import (get_my_schedule_service,
                                          request_schedule_change_service)
from src.utils.utils import check_xss_violation, format_api_response

doctors_namespace = Namespace("doctors", description="Chức năng riêng của bác sĩ")

work_schedule_detail_model = doctors_namespace.model('WorkScheduleDetail', {
    'title': fields.String(description='Tiêu đề lịch', example='Lịch làm việc mùa hè'),
    'description': fields.String(description='Mô tả chi tiết'),
    'start_time': fields.String(required=True, description='Giờ bắt đầu (HH:MM:SS)'),
    'end_time': fields.String(required=True, description='Giờ kết thúc (HH:MM:SS)'),
    'work_date': fields.List(fields.String, description='Danh sách các ngày trong tuần')
})

schedule_change_request_model = doctors_namespace.model('ScheduleChangeRequest', {
    'newWorkSchedule': fields.Nested(work_schedule_detail_model, required=True)
})


class RetrieveMyScheduleAPI(Resource):
    method_decorators = [token_required]

    @doctors_namespace.doc(security='api_key')
    def get(self, current_user):
        return format_api_response(*get_my_schedule_service(current_user))


class ScheduleRequestAPI(Resource):
    method_decorators = [token_required]

    @doctors_namespace.doc(security='api_key')
    @doctors_namespace.expect(schedule_change_request_model)
    def post(self, current_user):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation([data.get("reason", "")]):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *request_schedule_change_service(current_user, data), success_code=201
        )
