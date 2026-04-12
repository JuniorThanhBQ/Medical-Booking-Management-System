from flask import request
from flask_restx import Resource, fields

from src.middlewares.auth import auth_required
from src.modules.doctors import doctors_namespace, public_namespace
from src.modules.doctors.services import (get_doctor_detail_service,
                                          get_doctors_service,
                                          get_medical_service_detail_service,
                                          get_medical_services_service,
                                          get_my_schedule_service,
                                          get_specialties_service,
                                          get_specialty_detail_service,
                                          get_time_slots_service,
                                          request_schedule_change_service)
from src.utils.utils import check_xss_violation, format_api_response

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
    method_decorators = [auth_required]

    @doctors_namespace.doc(security='api_key')
    def get(self, current_user):
        return format_api_response(*get_my_schedule_service(current_user))


class ScheduleRequestAPI(Resource):
    method_decorators = [auth_required]

    @doctors_namespace.doc(security='api_key')
    @doctors_namespace.expect(schedule_change_request_model)
    def post(self, current_user):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation([data.get("reason", "")]):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *request_schedule_change_service(current_user, data), success_code=201
        )


class PublicSpecialtyListAPI(Resource):
    @public_namespace.doc(params={'keywords': 'Tên chuyên khoa cần lọc'})
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("limit", 5, type=int)
        keywords = request.args.get("keywords", type=str)

        data, message = get_specialties_service(
            page=page, per_page=per_page, keywords=keywords
        )

        return {
            "message": message,
            "data": data
        }, 200


class PublicSpecialtyRetrieveAPI(Resource):
    def get(self, specialty_id):
        return format_api_response(*get_specialty_detail_service(specialty_id))


class PublicMedicalServiceListAPI(Resource):
    @public_namespace.doc(params={'keywords': 'Tên dịch vụ cần tìm', 'specialtyId': 'ID Chuyên khoa'})
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("limit", 5, type=int)
        keywords = request.args.get("keywords", type=str)
        specialty_id = request.args.get("specialtyId", type=int)

        data, message = get_medical_services_service(
            page=page, per_page=per_page, keywords=keywords, specialty_id=specialty_id
        )

        return {
            "message": message,
            "data": data
        }, 200


class PublicMedicalServiceRetrieveAPI(Resource):
    def get(self, service_id):
        return format_api_response(*get_medical_service_detail_service(service_id))


class PublicDoctorListAPI(Resource):
    @public_namespace.doc(params={'keywords': 'Tên bác sĩ cần tìm'
        , 'specialtyId': 'mã chuyên khoa'
        , 'workDates': 'Các ngày làm việc'})
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("limit", 5, type=int)
        keywords = request.args.get("keywords", type=str)
        specialty_id = request.args.get("specialtyId", type=int)
        work_dates = request.args.getlist("workDates", type=int)

        data, message = get_doctors_service(
            page=page, per_page=per_page, keywords=keywords, specialty_id=specialty_id, work_dates=work_dates
        )

        return {
            "message": message,
            "data": data
        }, 200


class PublicDoctorRetrieveAPI(Resource):
    def get(self, doctor_id):
        return format_api_response(*get_doctor_detail_service(doctor_id))


class PublicDoctorSlotListAPI(Resource):
    @public_namespace.doc(params={'date': 'Ngày muốn xem lịch. Định dạng: YYYY-MM-DD',
                                  'serviceId': 'Mã dịch vụ y tế'})
    def get(self, doctor_id):
        date_str = request.args.get("date")
        service_id = request.args.get("serviceId", type=int)
        return format_api_response(*get_time_slots_service(doctor_id, date_str, service_id))
