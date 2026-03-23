from src import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.medical_records.models import MedicalRecord
from src.utils.decorator import handle_db_errors


@handle_db_errors(parameter=2)
def get_detail_medical_record_service(current_user, record_id):
    record = MedicalRecord.query.get(int(record_id))
    if not record:
        return {"message": "Phiếu khám không tồn tại"}, "NOT_FOUND"

    role_name = current_user.role.name
    profile_id = current_user.profile.id if current_user.profile else None

    if role_name == "PATIENT" and record.patient_profile_id != profile_id:
        return {"message": "Không có quyền truy cập"}, "FORBIDDEN"

    if role_name == "DOCTOR" and record.doctor_profile_id != profile_id:
        return {"message": "Không có quyền truy cập"}, "FORBIDDEN"

    appointment = record.appointment
    doctor_user = record.doctor.user
    patient_user = record.patient.user
    specialty = record.doctor.specialty

    result = {
        "id": str(record.id),
        "type": specialty.cta_label.name if specialty and specialty.cta_label else None,
        "appointmentId": str(appointment.id) if appointment else None,
        "patientName": f"{patient_user.last_name} {patient_user.first_name}",
        "doctorName": f"{doctor_user.last_name} {doctor_user.first_name}",
        "specialty": specialty.name if specialty else None,
        "status": appointment.status.name if appointment and appointment.status else None,
        "diagnosis": record.diagnosis,
        "notes": record.note,
        "prescriptionText": record.prescription_text,
        "treatmentOrders": record.treatment_orders,
        "createdAt": record.created_date.isoformat() + "Z" if record.created_date else None,
        "updatedAt": record.updated_date.isoformat() + "Z" if record.updated_date else None,
    }
    return result, "SUCCESS"

@handle_db_errors(parameter=2)
def create_medical_record_service(current_user, appointment_id, data):
    if current_user.role.name != "DOCTOR":
        return {"message": "Chỉ bác sĩ mới có quyền này"}, "FORBIDDEN"

    appointment = Appointment.query.get(int(appointment_id))
    if not appointment:
        return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

    if appointment.doctor_profile_id != current_user.profile.id:
        return {"message": "Không có quyền trên lịch hẹn này"}, "FORBIDDEN"

    record = appointment.medical_record
    if not record:
        record = MedicalRecord(
            doctor_profile_id=appointment.doctor_profile_id,
            patient_profile_id=appointment.patient_profile_id,
            diagnosis=data.get("diagnosis", ""),
            prescription_text=data.get("prescriptionText", ""),
            treatment_orders=data.get("treatmentOrders", ""),
            note=data.get("notes", ""),
        )
        db.session.add(record)
        db.session.flush()
        appointment.medical_record_id = record.id

    record.diagnosis = data.get("diagnosis", record.diagnosis)
    record.prescription_text = data.get("prescriptionText", record.prescription_text)
    record.treatment_orders = data.get("treatmentOrders", record.treatment_orders)
    record.note = data.get("notes", record.note)

    payload_status = data.get("status")
    if payload_status in ["DONE", "FOLLOW_UP"]:
        appointment.status = StatusRole.COMPLETED

    db.session.commit()
    return "", "SUCCESS"

@handle_db_errors(parameter=2)
def update_medical_record_service(current_user, record_id, data):
    if current_user.role.name != "DOCTOR":
        return {"message": "Chỉ bác sĩ mới có quyền này"}, "FORBIDDEN"

    record = MedicalRecord.query.get(int(record_id))
    if not record:
        return {"message": "Phiếu khám không tồn tại"}, "NOT_FOUND"

    if record.doctor_profile_id != current_user.profile.id:
        return {"message": "Không có quyền chỉnh sửa"}, "FORBIDDEN"

    if "diagnosis" in data:
        record.diagnosis = data["diagnosis"]

    if "prescriptionText" in data:
        record.prescription_text = data["prescriptionText"]

    if "treatmentOrders" in data:
        record.treatment_orders = data["treatmentOrders"]

    if "notes" in data:
        record.note = data["notes"]

    payload_status = data.get("status")
    if payload_status in ["DONE", "FOLLOW_UP"] and record.appointment:
        record.appointment.status = StatusRole.COMPLETED

    db.session.commit()
    return "", "SUCCESS"
