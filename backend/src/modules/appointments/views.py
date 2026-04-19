from dependency_injector.wiring import Provide, inject
from flask import request
from flask_restx import Namespace, Resource, fields

from src.containers import AppContainer
from src.middlewares.auth import auth_required
from src.utils.utils import check_xss_violation, format_api_response

appointments_namespace = Namespace("appointments", description="Các API lịch hẹn")

transaction_lock_model = appointments_namespace.model('TransactionLockRequest', {
    'doctorName': fields.String(required=True),
    'appointmentDate': fields.String(required=True),
    'serviceName': fields.String()
})

appointment_request_model = appointments_namespace.model('AppointmentRequest', {
    'doctorId': fields.Integer(required=True, description='ID của bác sĩ'),
    'medicalServiceId': fields.Integer(required=True, description='ID của dịch vụ y tế'),
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
    'medicalServiceId': fields.Integer(required=True, description='ID của dịch vụ y tế'),
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
    @inject
    def get(self, current_user, appointment_service=Provide[AppContainer.appointment_app.service]):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("limit", 10, type=int)

        return format_api_response(
            *appointment_service.get_appointments_list_service(current_user, page=page, per_page=per_page)
        )

    @appointments_namespace.doc(security='api_key')
    @appointments_namespace.expect(appointment_request_model)
    @inject
    def post(self, current_user, appointment_service=Provide[AppContainer.appointment_app.service]):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *appointment_service.create_patient_appointment_service(current_user, data),
            success_code=201
        )


class AppointmentRetrieveUpdateDeleteAPI(Resource):
    method_decorators = [auth_required]

    @appointments_namespace.doc(security='api_key')
    @inject
    def get(self, current_user, appointment_id, appointment_service=Provide[AppContainer.appointment_app.service]):
        return format_api_response(
            *appointment_service.get_appointment_detail_service(current_user, appointment_id)
        )

    @appointments_namespace.doc(security='api_key')
    @appointments_namespace.expect(patch_appointment_request_model)
    @inject
    def patch(self, current_user, appointment_id, appointment_service=Provide[AppContainer.appointment_app.service]):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *appointment_service.patch_appointment_service(current_user, appointment_id, data),
            success_code=204
        )

    @appointments_namespace.doc(security='api_key')
    @inject
    def delete(self, current_user, appointment_id, appointment_service=Provide[AppContainer.appointment_app.service]):
        return format_api_response(
            *appointment_service.delete_appointment_service(current_user, appointment_id),
            success_code=204
        )


class PatientRetrieveAPI(Resource):
    method_decorators = [auth_required]

    @appointments_namespace.doc(security='api_key')
    @inject
    def get(self, current_user, appointment_id, appointment_service=Provide[AppContainer.appointment_app.service]):
        return format_api_response(
            *appointment_service.get_patient_profile_service(current_user, appointment_id)
        )


class ReceptionistAppointmentCreateAPI(Resource):
    method_decorators = [auth_required]

    @appointments_namespace.doc(security='api_key')
    @appointments_namespace.expect(receptionist_appointment_model)
    @inject
    def post(self, current_user, appointment_service=Provide[AppContainer.appointment_app.service]):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *appointment_service.create_receptionist_appointment_service(current_user, data),
            success_code=201
        )


class TransactionLockAPI(Resource):
    @appointments_namespace.expect(transaction_lock_model)
    @inject
    def post(self, appointment_service=Provide[AppContainer.appointment_app.service]):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *appointment_service.lock_booking_transaction_service(data),
            success_code=204
        )


class TransactionUnlockAPI(Resource):
    @appointments_namespace.expect(transaction_lock_model)
    @inject
    def post(self, appointment_service=Provide[AppContainer.appointment_app.service]):
        data = request.get_json(silent=True) or request.form.to_dict()

        if check_xss_violation(data.values()):
            return {"message": "Dữ liệu đầu vào chứa ký tự không hợp lệ"}, 400

        return format_api_response(
            *appointment_service.unlock_booking_transaction_service(data),
            success_code=204
        )
