from flask import request
from flask_restx import Resource, fields

from src.middlewares.auth import auth_required
from src.modules.medical_records import medical_records_namespace
from src.modules.medical_records.services import (
    create_medical_record_service, get_detail_medical_record_service,
    get_list_medical_record_service, update_medical_record_service)
from src.utils.utils import check_xss_violation, format_api_response

update_medical_record_model = medical_records_namespace.model('UpdateMedicalRecordRequest', {
    'diagnosis': fields.String(description='Chẩn đoán của bác sĩ'),
    'prescriptionText': fields.String(description='Thông tin đơn thuốc'),
    'treatmentOrders': fields.String(description='Yêu cầu điều trị/Xét nghiệm'),
    'notes': fields.String(description='Ghi chú thêm'),
    'status': fields.String(description='Trạng thái hồ sơ (DONE, FOLLOW_UP)')
})
medical_record_result_model = medical_records_namespace.model('MedicalRecordResponse', {
    'id': fields.Integer(description='ID của hồ sơ bệnh án'),
    'diagnosis': fields.String(description='Chẩn đoán'),
    'prescriptionText': fields.String(description='Đơn thuốc'),
    'treatmentOrders': fields.String(description='Yêu cầu điều trị'),
    'notes': fields.String(description='Ghi chú'),
    'status': fields.String(description='Trạng thái hiện tại của hồ sơ')
})
create_medical_record_model = medical_records_namespace.model('CreateMedicalRecordRequest', {
    'diagnosis': fields.String(description='Chẩn đoán ban đầu'),
    'prescriptionText': fields.String(description='Nội dung đơn thuốc', ),
    'treatmentOrders': fields.String(description='Yêu cầu điều trị/xét nghiệm'),
    'notes': fields.String(description='Ghi chú của bác sĩ'),
    'status': fields.String(description='Trạng thái (DONE hoặc FOLLOW_UP)', default='DONE')
})
medical_record_response_model = medical_records_namespace.model('MedicalRecordCreateResponse', {
    'id': fields.Integer(description='ID của hồ sơ vừa tạo'),
    'diagnosis': fields.String(description='Chẩn đoán'),
    'prescriptionText': fields.String(description='Đơn thuốc'),
    'treatmentOrders': fields.String(description='Yêu cầu điều trị'),
    'notes': fields.String(description='Ghi chú'),
    'status': fields.String(description='Trạng thái hồ sơ')
})


class MedicalRecordListAPI(Resource):
    method_decorators = [auth_required]

    @medical_records_namespace.doc(security='api_key')
    def get(self, current_user):
        args = request.args.to_dict()
        return format_api_response(
            *get_list_medical_record_service(current_user, args)
        )


class MedicalRecordRetrieveUpdateAPI(Resource):
    method_decorators = [auth_required]

    @medical_records_namespace.doc(security='api_key')
    def get(self, current_user, medical_record_id):
        return format_api_response(
            *get_detail_medical_record_service(current_user, medical_record_id)
        )

    @medical_records_namespace.doc(security='api_key')
    @medical_records_namespace.expect(update_medical_record_model)
    def patch(self, current_user, medical_record_id):
        data = request.get_json(silent=True) or request.form.to_dict()
        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *update_medical_record_service(current_user, medical_record_id, data))


class CreateMedicalRecordAPI(Resource):
    method_decorators = [auth_required]

    @medical_records_namespace.doc(security='api_key')
    @medical_records_namespace.expect(create_medical_record_model)
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
