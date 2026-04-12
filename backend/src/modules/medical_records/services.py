from src.modules.appointments.models import StatusRole
from src.modules.appointments.repositories import get_appointment_by_id
from src.modules.medical_records.models import MedicalRecord, MedicalRecordType
from src.modules.medical_records.repositories import (
    add_instance, commit_session, flush_session, get_medical_record_by_id,
    get_medical_records_by_role)
from src.utils.handle_db_errors import handle_db_errors


def format_medical_record(record):
    appointment = record.appointment
    doctor_user = record.doctor.user
    patient_user = record.patient.user
    specialty = record.doctor.specialty

    return {
        "id": str(record.id),
        "service": appointment.medical_service.name if appointment and appointment.medical_service else None,
        "appointmentId": str(appointment.id) if appointment else None,
        "patientName": f"{patient_user.last_name} {patient_user.first_name}",
        "doctorName": f"{doctor_user.last_name} {doctor_user.first_name}",
        "specialty": specialty.name if specialty else None,
        "status": appointment.status.name if appointment and appointment.status else None,
        "diagnosis": record.diagnosis,
        "createdAt": record.created_date.isoformat() + "Z" if record.created_date else None,
    }


def _check_record_access_permission(current_user, record):
    role_name = current_user.role.name
    profile_id = current_user.profile.id if current_user.profile else None

    if role_name == "PATIENT" and record.patient_profile_id != profile_id:
        return False
    if role_name == "DOCTOR" and record.doctor_profile_id != profile_id:
        return False
    return True


@handle_db_errors
def create_medical_record_service(current_user, appointment_id, data):
    if current_user.role.name != "DOCTOR":
        return {"message": "Chỉ bác sĩ mới có quyền này"}, "FORBIDDEN"

    appointment = get_appointment_by_id(appointment_id)
    if not appointment:
        return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

    if appointment.doctor_profile_id != current_user.profile.id:
        return {"message": "Không có quyền trên lịch hẹn này"}, "FORBIDDEN"

    if appointment.medical_record:
        return {"message": "Lịch hẹn này đã có hồ sơ bệnh án."}, "BAD_REQUEST"

    payload_status = data.get("status", "DONE")
    if payload_status not in ["DONE", "FOLLOW_UP"]:
        return {"message": "Trạng thái không hợp lệ"}, "BAD_REQUEST"

    record = MedicalRecord(
        doctor_profile_id=appointment.doctor_profile_id,
        patient_profile_id=appointment.patient_profile_id,
        type=MedicalRecordType[payload_status],
        diagnosis=data.get("diagnosis", ""),
        prescription_text=data.get("prescriptionText", ""),
        treatment_orders=data.get("treatmentOrders", ""),
        note=data.get("notes", "")
    )

    add_instance(record)
    flush_session()

    appointment.medical_record_id = record.id
    appointment.status = StatusRole.COMPLETED

    commit_session()

    result = {
        "id": record.id,
        "diagnosis": record.diagnosis,
        "prescriptionText": record.prescription_text,
        "treatmentOrders": record.treatment_orders,
        "notes": record.note,
        "status": record.type.name
    }

    return result, "SUCCESS"


@handle_db_errors
def update_medical_record_service(current_user, record_id, data):
    if current_user.role.name != "DOCTOR":
        return {"message": "Chỉ bác sĩ mới có quyền này"}, "FORBIDDEN"

    record = get_medical_record_by_id(record_id)
    if not record:
        return {"message": "Phiếu khám không tồn tại"}, "NOT_FOUND"

    if record.doctor_profile_id != current_user.profile.id:
        return {"message": "Không có quyền chỉnh sửa"}, "FORBIDDEN"

    field_mapping = {
        "diagnosis": "diagnosis",
        "prescriptionText": "prescription_text",
        "treatmentOrders": "treatment_orders",
        "notes": "note"
    }

    for payload_key, model_attr in field_mapping.items():
        if payload_key in data:
            setattr(record, model_attr, data[payload_key])

    payload_status = data.get("status")
    if payload_status in ["DONE", "FOLLOW_UP"]:
        record.type = MedicalRecordType[payload_status]
        if record.appointment:
            record.appointment.status = StatusRole.COMPLETED

    commit_session()

    result = {
        "id": record.id,
        "diagnosis": record.diagnosis,
        "prescriptionText": record.prescription_text,
        "treatmentOrders": record.treatment_orders,
        "notes": record.note,
        "status": record.type.name if record.type else None
    }

    return result, "SUCCESS"


@handle_db_errors
def get_detail_medical_record_service(current_user, record_id):
    record = get_medical_record_by_id(record_id)
    if not record:
        return {"message": "Phiếu khám không tồn tại"}, "NOT_FOUND"

    if not _check_record_access_permission(current_user, record):
        return {"message": "Không có quyền truy cập"}, "FORBIDDEN"

    result = format_medical_record(record)
    result.update({
        "notes": record.note,
        "prescriptionText": record.prescription_text,
        "treatmentOrders": record.treatment_orders,
        "updatedAt": record.updated_date.isoformat() + "Z" if record.updated_date else None,
    })

    return result, "SUCCESS"


@handle_db_errors
def get_list_medical_record_service(current_user, args):
    role_name = current_user.role.name

    if role_name == "RECEPTIONIST":
        return {"message": "Lễ tân không thể xem danh sách hồ sơ khám bệnh"}, "FORBIDDEN"

    profile_id = current_user.profile.id if current_user.profile else None

    if role_name in ["PATIENT", "DOCTOR"] and not profile_id:
        return {"message": "Tài khoản chưa có hồ sơ để xem bệnh án"}, "FORBIDDEN"

    page = int(args.get("page", 1))
    limit = int(args.get("limit", 10))

    paginated_records = get_medical_records_by_role(
        role_name=role_name,
        profile_id=profile_id,
        page=page,
        limit=limit
    )

    items = [format_medical_record(record) for record in paginated_records.items]

    result = {
        "items": items,
        "meta": {
            "total": paginated_records.total,
            "pages": paginated_records.pages,
            "currentPage": paginated_records.page,
            "perPage": paginated_records.per_page
        }
    }
    return result, "SUCCESS"
