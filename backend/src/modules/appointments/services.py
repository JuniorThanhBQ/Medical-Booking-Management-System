from src.extensions import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.public.services import get_available_time_slots
from src.utils.decorator import handle_db_errors
from src.utils.utils import (format_appointment_response,
                             format_appointment_summary,
                             parse_appointment_datetime,
                             validate_appointment_booking,
                             validate_appointment_date,
                             validate_available_slot)

@handle_db_errors(parameter=2)
def get_appointments_list_service(current_user, page=1, per_page=10):
    role_name = current_user.role.name
    query = Appointment.query

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
                "patientName": f"{patient_user.last_name} {patient_user.first_name}",
                "doctorName": f"{doctor_user.last_name} {doctor_user.first_name}",
                "status": appointment.status.name if appointment.status else None,
                "appointmentDate": appointment.appointment_date.isoformat() + "Z",
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

@handle_db_errors(parameter=2)
def get_appointment_detail_service(current_user, appointment_id):
    appointment = db.session.get(Appointment, int(appointment_id))
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
    specialty = appointment.doctor.specialty

    appointment_data = format_appointment_summary(appointment, patient_user, doctor_user, specialty)
    result = {
        **appointment_data,
        "medicalRecordId": str(appointment.medical_record_id) ,
    }
    return result, "SUCCESS"

@handle_db_errors(parameter=2)
def get_patient_profile_service(current_user, appointment_id):
    if current_user.role.name != "DOCTOR":
        return {"message": "Chỉ bác sĩ mới có quyền này"}, "FORBIDDEN"

    appointment = db.session.get(Appointment, int(appointment_id))
    if not appointment:
        return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

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

@handle_db_errors(parameter=2)
# pylint: disable=too-many-return-statements
def create_patient_appointment_service(current_user, data):
    if current_user.role.name != "PATIENT":
        return {"message": "Chỉ bệnh nhân mới được đặt lịch"}, "FORBIDDEN"

    doctor_id = data.get("doctorId")
    appointment_date_str = data.get("appointmentDate")
    note = data.get("note", "")

    if not doctor_id or not appointment_date_str:
        return {"message": "Thiếu thông tin bắt buộc"}, "ERROR_BAD_REQUEST"

    appointment_dt, doctor, error = validate_appointment_booking(
        doctor_id, appointment_date_str, get_available_time_slots, db.session
    )
    if error:
        if isinstance(error, tuple):
            return error
        return error

    new_appointment = Appointment(
        name=f"Khám bệnh - {current_user.last_name} {current_user.first_name}",
        note=note,
        status=StatusRole.APPROVED,
        appointment_date=appointment_dt,
        doctor_profile_id=doctor.profile.id,
        patient_profile_id=current_user.profile.id,
    )
    db.session.add(new_appointment)
    db.session.commit()

    response = format_appointment_response(
        new_appointment, doctor, f"{current_user.last_name} {current_user.first_name}")
    return response, "SUCCESS"


@handle_db_errors(parameter=2)
# pylint: disable=too-many-return-statements
def patch_appointment_service(current_user, appointment_id, data):
    if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
        return {"message": "Không có quyền thực hiện"}, "FORBIDDEN"

    appointment = db.session.get(Appointment, int(appointment_id))
    if not appointment:
        return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

    if "status" in data:
        try:
            appointment.status = StatusRole[data["status"].upper()]
        except KeyError:
            return {"message": "Trạng thái không hợp lệ"}, "ERROR_BAD_REQUEST"

    appointment.note = data["note"]

    if "appointmentDate" in data:
        appointment_date_str = data["appointmentDate"]
        appointment_dt, error = parse_appointment_datetime(appointment_date_str)
        if error:
            return error

        error, status = validate_appointment_date(appointment_dt)
        if error:
            return error, status

        if appointment.appointment_date != appointment_dt:
            doctor = appointment.doctor.user
            target_date = appointment_dt.date()
            available_slots = get_available_time_slots(doctor, target_date)
            error, status = validate_available_slot(appointment_dt, available_slots)
            if error:
                return error, status
            appointment.appointment_date = appointment_dt

    db.session.commit()
    return "", "SUCCESS"


@handle_db_errors(parameter=2)
def delete_appointment_service(current_user, appointment_id):
    if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
        return {"message": "Không có quyền thực hiện"}, "FORBIDDEN"

    appointment = db.session.get(Appointment, int(appointment_id))
    if not appointment:
        return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

    if appointment.status != StatusRole.CANCEL:
        return {"message": "Chỉ được phép xóa lịch hẹn ở trạng thái đã hủy"}, "ERROR_BAD_REQUEST"

    db.session.delete(appointment)
    db.session.commit()

    return "", "SUCCESS"
