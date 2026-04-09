from flask import request
from flask_restx import Namespace, Resource, fields

from src.middlewares.auth import auth_required
from src.modules.appointments.services import (
    create_medical_record_service, create_patient_appointment_service,
    create_receptionist_appointment_service, delete_appointment_service,
    get_appointment_detail_service, get_appointments_list_service,
    get_detail_medical_record_service, get_patient_profile_service,
    get_time_slots_service, patch_appointment_service,
    update_medical_record_service)
from src.utils.utils import check_xss_violation, format_api_response

appointments_namespace = Namespace("appointments", description="Các API lịch hẹn")
public_namespace = Namespace("public", description="Các API không cần đăng nhập")
medical_records_namespace = Namespace("medical_records", description="Các API hồ sơ bệnh án")

appointment_request_model = appointments_namespace.model('AppointmentRequest', {
    'doctorId': fields.Integer(required=True, description='ID của bác sĩ'),
    'appointmentDate': fields.String(required=True, description='Thời gian hẹn (ISO 8601)'),
    'note': fields.String(description='Ghi chú hoặc triệu chứng ban đầu')
})

patch_appointment_request_model = appointments_namespace.model('PatchAppointmentRequest', {
    'status': fields.String(description='Trạng thái mới (APPROVED, COMPLETED, CANCEL, PENDING)'),
    'note': fields.String(description='Cập nhật ghi chú'),
    'appointmentDate': fields.String(description='Thời gian hẹn mới (ISO 8601)')
})

receptionist_appointment_model = appointments_namespace.model('ReceptionistAppointmentRequest', {
    'doctorId': fields.Integer(required=True, description='ID của bác sĩ'),
    'appointmentDate': fields.String(required=True, description='ISO 8601 format'),
    'note': fields.String(description='Ghi chú khám bệnh'),
    'firstName': fields.String(required=True),
    'lastName': fields.String(required=True),
    'phone': fields.String(required=True),
    'gender': fields.String(required=True, description='MALE, FEMALE, or OTHER'),
    'birthday': fields.String(required=True, description='YYYY-MM-DD'),
    'address': fields.String(required=True)
})


class AppointmentListCreateAPI(Resource):
    method_decorators = [auth_required]

    @appointments_namespace.doc(security='api_key')
    def get(self, current_user):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("limit", 10, type=int)

        return format_api_response(
            *get_appointments_list_service(current_user, page=page, per_page=per_page)
        )

    @appointments_namespace.doc(security='api_key')
    @appointments_namespace.expect(appointment_request_model)
    def post(self, current_user):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *create_patient_appointment_service(current_user, data),
            success_code=201
        )


class AppointmentRetrieveUpdateDeleteAPI(Resource):
    method_decorators = [auth_required]

    @appointments_namespace.doc(security='api_key')
    def get(self, current_user, appointment_id):
        return format_api_response(
            *get_appointment_detail_service(current_user, appointment_id)
        )

    @appointments_namespace.doc(security='api_key')
    @appointments_namespace.expect(patch_appointment_request_model)
    def patch(self, current_user, appointment_id):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *patch_appointment_service(current_user, appointment_id, data),
            success_code=204
        )

    @appointments_namespace.doc(security='api_key')
    def delete(self, current_user, appointment_id):
        return format_api_response(
            *delete_appointment_service(current_user, appointment_id),
            success_code=204
        )


class PatientRetrieveAPI(Resource):
    method_decorators = [auth_required]

    @appointments_namespace.doc(security='api_key')
    def get(self, current_user, appointment_id):
        return format_api_response(
            *get_patient_profile_service(current_user, appointment_id)
        )


class ReceptionistAppointmentCreateAPI(Resource):
    method_decorators = [auth_required]

    @appointments_namespace.doc(security='api_key')
    @appointments_namespace.expect(receptionist_appointment_model)
    def post(self, current_user):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *create_receptionist_appointment_service(current_user, data),
            success_code=201
        )


class PublicDoctorSlotListAPI(Resource):
    @public_namespace.doc(params={'date': 'Ngày muốn xem lịch. Định dạng: YYYY-MM-DD'})
    def get(self, doctor_id):
        date_str = request.args.get("date")
        return format_api_response(*get_time_slots_service(doctor_id, date_str))


medical_records_namespace = Namespace("medical-records", description="Quản lý hồ sơ bệnh án")
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
