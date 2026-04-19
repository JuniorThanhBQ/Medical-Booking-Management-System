from datetime import datetime

from src.modules.appointments.models import Appointment, StatusRole
from src.modules.users.models import GenderRole
from src.utils.appointment.appointment_validate_utils import (
    validate_appointment_date, validate_available_slot, validate_doctor)
from src.utils.appointment.formatter_utils import (format_appointment,
                                                   parse_appointment_datetime)
from src.utils.handle_db_errors import handle_db_errors


def handle_status_update(appointment, status_name):
    if not status_name:
        return None
    try:
        appointment.status = StatusRole[status_name.upper()]
        return None
    except KeyError:
        return {"message": "Trạng thái không hợp lệ"}, "ERROR_BAD_REQUEST"


class AppointmentService:
    def __init__(self, appointment_repository, doctor_repository, doctor_service):
        self.appointment_repository = appointment_repository
        self.doctor_repository = doctor_repository
        self.doctor_service = doctor_service

    def validate_appointment_booking(self, doctor_id, str_appointment_date, medical_service_id):
        appointment_datetime, parsed_error = parse_appointment_datetime(str_appointment_date)

        if parsed_error:
            return None, None, None, parsed_error

        input_date_error, status = validate_appointment_date(appointment_datetime)

        if input_date_error:
            return None, None, None, (input_date_error, status)

        doctor = self.doctor_repository.get_doctor_by_id(doctor_id)
        not_found_error, status = validate_doctor(doctor)

        if not_found_error:
            return None, None, None, (not_found_error, status)

        medical_service = self.doctor_repository.get_medical_service_by_id(medical_service_id)
        if not medical_service:
            return None, None, None, ({"message": "Dịch vụ y tế không tồn tại"}, "NOT_FOUND")

        if doctor.profile.specialty_id != medical_service.specialty_id:
            return None, None, None, ({"message": "Bác sĩ không cung cấp dịch vụ này"}, "ERROR_BAD_REQUEST")

        target_date = appointment_datetime.date()
        available_slots = self.doctor_service.get_available_time_slots(doctor, target_date, medical_service)
        validate_error, status = validate_available_slot(appointment_datetime, available_slots)

        if validate_error:
            return None, None, None, (validate_error, status)

        return appointment_datetime, doctor, medical_service, None

    def get_or_create_patient_profile(self, data):
        try:
            birthday_dt = datetime.strptime(data.get("birthday"), "%Y-%m-%d").date()
            gender_enum = GenderRole[data.get("gender").upper()]
        except (ValueError, KeyError, AttributeError):
            return None, ({"message": "Thông tin ngày sinh hoặc giới tính không hợp lệ"},
                          "ERROR_BAD_REQUEST")

        patient_profile = self.appointment_repository.get_patient_profile_by_details(
            data.get("firstName"),
            data.get("lastName"),
            data.get("phone"),
            gender_enum,
            birthday_dt,
            data.get("address")
        )

        if not patient_profile:
            patient_profile = self.appointment_repository.create_new_patient_profile(
                data.get("firstName"),
                data.get("lastName"),
                data.get("phone"),
                gender_enum,
                birthday_dt,
                data.get("address")
            )

        return patient_profile, None

    def validate_appointment_request(self, current_user, data):
        if current_user.role.name != "PATIENT":
            return None, None, None, ({"message": "Chỉ bệnh nhân mới được đặt lịch"}, "FORBIDDEN")

        doctor_id = data.get("doctorId")
        appointment_date_str = data.get("appointmentDate")
        medical_service_id = data.get("medicalServiceId")

        if not doctor_id or not appointment_date_str or not medical_service_id:
            return None, None, None, ({"message": "Thiếu thông tin bắt buộc"}, "ERROR_BAD_REQUEST")

        appointment_date, doctor, medical_service, error = self.validate_appointment_booking(
            doctor_id, appointment_date_str, medical_service_id
        )

        return appointment_date, doctor, medical_service, error

    def handle_date_update(self, appointment, date_str):
        if not date_str:
            return None

        appointment_date, error = parse_appointment_datetime(date_str)
        if error:
            return error

        val_error, status = validate_appointment_date(appointment_date)
        if val_error:
            return val_error, status

        if appointment.appointment_date != appointment_date:
            doctor_user = appointment.doctor.user
            available_slots = self.doctor_service.get_available_time_slots(
                doctor_user, appointment_date.date(), appointment.medical_service
            )

            slot_error, slot_status = validate_available_slot(appointment_date, available_slots)
            if slot_error:
                return slot_error, slot_status

            appointment.appointment_date = appointment_date
        return None

    @handle_db_errors
    def get_appointments_list_service(self, current_user, page=1, per_page=5):
        role_name = current_user.role.name
        query = self.appointment_repository.get_appointments_base_query()

        empty_result = {
            "items": [],
            "meta": {
                "total": 0,
                "pages": 0,
                "currentPage": page,
                "perPage": per_page,
                "hasNext": False,
                "hasPrev": False
            }
        }

        if role_name == "PATIENT":
            if not current_user.profile:
                return empty_result, "SUCCESS"
            query = query.filter(Appointment.patient_profile_id == current_user.profile.id)
        elif role_name == "DOCTOR":
            if not current_user.profile:
                return empty_result, "SUCCESS"
            query = query.filter(Appointment.doctor_profile_id == current_user.profile.id)
        elif role_name in ["RECEPTIONIST", "ADMIN"]:
            pass
        else:
            return {"message": "Không có quyền truy cập"}, "FORBIDDEN"

        pagination = query.order_by(Appointment.appointment_date.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        items = []
        for appointment in pagination.items:
            doctor_user = appointment.doctor.user
            patient_user = appointment.patient.user
            items.append(
                {
                    "id": str(appointment.id),
                    "name": appointment.name,
                    "patientName": f"{patient_user.last_name} {patient_user.first_name}",
                    "doctorName": f"{doctor_user.last_name} {doctor_user.first_name}",
                    "status": appointment.status.name if appointment.status else None,
                    "appointmentDate": appointment.appointment_date.isoformat() + "+07:00",
                }
            )

        result = {
            "items": items,
            "meta": {
                "total": pagination.total,
                "pages": pagination.pages,
                "currentPage": pagination.page,
                "perPage": pagination.per_page,
                "hasNext": pagination.has_next,
                "hasPrev": pagination.has_prev
            }
        }
        return result, "SUCCESS"

    @handle_db_errors
    def get_appointment_detail_service(self, current_user, appointment_id):
        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        if not appointment:
            return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

        role_name = current_user.role.name
        profile_id = current_user.profile.id if current_user.profile else None

        if role_name == "PATIENT" and appointment.patient_profile_id != profile_id:
            return {"message": "Không có quyền truy cập"}, "FORBIDDEN"

        if role_name == "DOCTOR" and appointment.doctor_profile_id != profile_id:
            return {"message": "Không có quyền truy cập"}, "FORBIDDEN"

        doctor_user = appointment.doctor.user
        patient_user = appointment.patient.user
        raw_specialty = appointment.doctor.specialty
        specialty_data = {"id": raw_specialty.id, "name": raw_specialty.name} if raw_specialty else None

        appointment_data = format_appointment(
            appointment=appointment,
            patient_user=patient_user,
            doctor=doctor_user,
            specialty=specialty_data
        )
        result = {
            **appointment_data,
            "medicalRecordId": str(appointment.medical_record_id) if appointment.medical_record_id else None,
        }
        return result, "SUCCESS"

    @handle_db_errors
    def get_patient_profile_service(self, current_user, appointment_id):
        if current_user.role.name not in ["DOCTOR", "RECEPTIONIST"]:
            return {"message": "Chỉ bác sĩ hoặc lễ tân mới có quyền này"}, "FORBIDDEN"

        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        if not appointment:
            return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

        if not current_user.role.name == "RECEPTIONIST":
            if appointment.doctor_profile_id != current_user.profile.id:
                return {"message": "Không có quyền trên lịch hẹn này"}, "FORBIDDEN"

        patient = appointment.patient
        user = patient.user

        result = {
            "firstName": user.first_name,
            "lastName": user.last_name,
            "dateOfBirth": patient.birthday.isoformat() if patient.birthday else None,
            "gender": patient.gender.name if patient.gender else None,
            "phone": patient.phone,
            "address": patient.address,
            "avatar": patient.avatar,
            "medicalHistory": patient.medical_history,
        }
        return result, "SUCCESS"

    @handle_db_errors
    def create_patient_appointment_service(self, current_user, data):
        appointment_date, doctor, medical_service, error = self.validate_appointment_request(current_user, data)
        if error:
            return error

        full_name = f"{current_user.last_name} {current_user.first_name}"
        formatted_date = appointment_date.strftime('%H:%M %d/%m')
        new_appointment = Appointment(
            name=f"LH - {full_name} - {formatted_date}",
            note=data.get("note", ""),
            status=StatusRole.APPROVED,
            appointment_date=appointment_date,
            doctor_profile_id=doctor.profile.id,
            patient_profile_id=current_user.profile.id,
            medical_service_id=medical_service.id
        )

        self.appointment_repository.add_instance(new_appointment)
        self.appointment_repository.commit_session()

        return format_appointment(appointment=new_appointment,
                                  doctor=doctor,
                                  patient_name=full_name), "SUCCESS"

    @handle_db_errors
    def patch_appointment_service(self, current_user, appointment_id, data):
        if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
            return {"message": "Không có quyền thực hiện"}, "FORBIDDEN"

        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        if not appointment:
            return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

        if "note" in data:
            appointment.note = data["note"]

        status_error = handle_status_update(appointment, data.get("status"))
        if status_error:
            return status_error

        date_error = self.handle_date_update(appointment, data.get("appointmentDate"))
        if date_error:
            return date_error

        self.appointment_repository.commit_session()
        return "", "SUCCESS"

    @handle_db_errors
    def delete_appointment_service(self, current_user, appointment_id):
        if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
            return {"message": "Chỉ lễ tân được thực hiện"}, "FORBIDDEN"

        appointment = self.appointment_repository.get_appointment_by_id(appointment_id)
        if not appointment:
            return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

        if appointment.status != StatusRole.CANCEL:
            return {"message": "Chỉ được phép xóa lịch hẹn ở trạng thái đã hủy"}, "ERROR_BAD_REQUEST"

        self.appointment_repository.delete_instance(appointment)
        self.appointment_repository.commit_session()
        return "", "SUCCESS"

    @handle_db_errors
    def create_receptionist_appointment_service(self, current_user, data):
        if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
            return {"message": "Không có quyền thực hiện"}, "FORBIDDEN"

        medical_service_id = data.get("medicalServiceId")
        if not medical_service_id:
            return {"message": "Thiếu mã dịch vụ y tế"}, "ERROR_BAD_REQUEST"

        appointment_date, doctor, medical_service, error = self.validate_appointment_booking(
            data.get("doctorId"), data.get("appointmentDate"), medical_service_id
        )
        if error:
            return error

        patient_profile, patient_error = self.get_or_create_patient_profile(data)
        if patient_error:
            return patient_error

        full_name = f"{data.get('lastName')} {data.get('firstName')}"
        formatted_date = appointment_date.strftime('%H:%M %d/%m')
        new_appointment = Appointment(
            name=f"LHLT - {full_name} - {formatted_date}",
            note=data.get("note", ""),
            status=StatusRole.APPROVED,
            appointment_date=appointment_date,
            doctor_profile_id=doctor.profile.id,
            patient_profile_id=patient_profile.id,
            medical_service_id=medical_service.id
        )

        self.appointment_repository.add_instance(new_appointment)
        self.appointment_repository.commit_session()

        return format_appointment(appointment=new_appointment, doctor=doctor, patient_name=full_name), "SUCCESS"

    @handle_db_errors
    def lock_booking_transaction_service(self, data):
        doctor_name = data.get("doctorName")
        appointment_date_str = data.get("appointmentDate")
        service_name = data.get("serviceName")

        if not doctor_name or not appointment_date_str:
            return {"message": "Thiếu thông tin bác sĩ hoặc thời gian"}, "ERROR_BAD_REQUEST"

        appointment_date, parsed_error = parse_appointment_datetime(appointment_date_str)
        if parsed_error:
            return parsed_error

        self.appointment_repository.clean_expired_booking_locks()
        self.appointment_repository.commit_session()

        existing_lock = self.appointment_repository.get_active_booking_lock(doctor_name, appointment_date)
        if existing_lock:
            return {"message": "Khung giờ này đang được người khác giữ chỗ"}, "CONFLICT"

        self.appointment_repository.create_booking_lock(doctor_name, appointment_date, service_name)
        self.appointment_repository.commit_session()

        return "", "SUCCESS"

    @handle_db_errors
    def unlock_booking_transaction_service(self, data):
        doctor_name = data.get("doctorName")
        appointment_date_str = data.get("appointmentDate")

        if not doctor_name or not appointment_date_str:
            return {"message": "Thiếu thông tin bác sĩ hoặc thời gian"}, "ERROR_BAD_REQUEST"

        appointment_date, parsed_error = parse_appointment_datetime(appointment_date_str)
        if parsed_error:
            return parsed_error

        self.appointment_repository.delete_booking_lock(doctor_name, appointment_date)
        self.appointment_repository.commit_session()

        return "", "SUCCESS"
