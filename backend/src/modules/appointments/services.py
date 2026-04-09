import uuid
from datetime import date, datetime, timedelta

from flask import current_app
from sqlalchemy import func
from werkzeug.security import generate_password_hash

from src.extensions import db
from src.modules.appointments.models import (Appointment, MedicalRecord,
                                             MedicalRecordType, StatusRole)
from src.modules.doctors.services import format_work_schedule, get_doctor_by_id
from src.modules.notification.signals import insert_appointment_notifications
from src.modules.shared.services import (check_is_conflicting,
                                         format_appointment, get_slot_duration,
                                         parse_appointment_datetime,
                                         validate_appointment_date,
                                         validate_available_slot)
from src.modules.users.models import GenderRole, PatientProfile, User, UserRole
from src.utils.handle_db_errors import handle_db_errors


@handle_db_errors
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
                "name": appointment.name,
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


@handle_db_errors
def get_appointment_detail_service(current_user, appointment_id):
    appointment = db.session.get(Appointment, int(appointment_id))
    if not appointment:
        return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

    role_name = current_user.role.name
    if current_user.profile:
        profile_id = current_user.profile.id
    else:
        profile_id = None

    if role_name == "PATIENT" and appointment.patient_profile_id != profile_id:
        return {"message": "Không có quyền truy cập"}, "FORBIDDEN"

    if role_name == "DOCTOR" and appointment.doctor_profile_id != profile_id:
        return {"message": "Không có quyền truy cập"}, "FORBIDDEN"

    doctor_user = appointment.doctor.user
    patient_user = appointment.patient.user
    specialty = appointment.doctor.specialty

    appointment_data = format_appointment(appointment, patient_user, doctor_user, specialty)
    result = {
        **appointment_data,
        "medicalRecordId": str(appointment.medical_record_id),
    }
    return result, "SUCCESS"


@handle_db_errors
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


def validate_appointment_request(current_user, data):
    if current_user.role.name != "PATIENT":
        return None, None, ({"message": "Chỉ bệnh nhân mới được đặt lịch"}, "FORBIDDEN")

    doctor_id = data.get("doctorId")
    appointment_date_str = data.get("appointmentDate")

    if not doctor_id or not appointment_date_str:
        return None, None, ({"message": "Thiếu thông tin bắt buộc"}, "ERROR_BAD_REQUEST")

    appointment_date, doctor, error = validate_appointment_booking(
        doctor_id, appointment_date_str, get_available_time_slots
    )

    return appointment_date, doctor, error

@handle_db_errors
def create_patient_appointment_service(current_user, data):
    appointment_date, doctor, error = validate_appointment_request(current_user, data)
    if error:
        return error

    current_app.config["DISABLE_SIGNALS"] = True
    full_name = f"{current_user.last_name} {current_user.first_name}"
    new_appointment = Appointment(
        name=f"KB - {appointment_date}",
        note=data.get("note", ""),
        status=StatusRole.APPROVED,
        appointment_date=appointment_date,
        doctor_profile_id=doctor.profile.id,
        patient_profile_id=current_user.profile.id,
    )

    db.session.add(new_appointment)
    db.session.commit()

    insert_appointment_notifications(new_appointment, action_name="chấp thuận")
    current_app.config["DISABLE_SIGNALS"] = False

    return format_appointment(appointment=new_appointment,
                              doctor=doctor,
                              patient_name=full_name), "SUCCESS"


def handle_status_update(appointment, status_name):
    if not status_name:
        return None
    try:
        appointment.status = StatusRole[status_name.upper()]
        return None
    except KeyError:
        return {"message": "Trạng thái không hợp lệ"}, "ERROR_BAD_REQUEST"


def handle_date_update(appointment, date_str):
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
        available_slots = get_available_time_slots(doctor_user, appointment_date.date())

        slot_error, slot_status = validate_available_slot(appointment_date, available_slots)
        if slot_error:
            return slot_error, slot_status

        appointment.appointment_date = appointment_date
    return None


@handle_db_errors
def patch_appointment_service(current_user, appointment_id, data):
    if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
        return {"message": "Không có quyền thực hiện"}, "FORBIDDEN"

    appointment = db.session.get(Appointment, int(appointment_id))
    if not appointment:
        return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

    current_app.config["DISABLE_SIGNALS"] = True

    if "note" in data:
        appointment.note = data["note"]

    status_error = handle_status_update(appointment, data.get("status"))
    if status_error:
        return status_error

    date_error = handle_date_update(appointment, data.get("appointmentDate"))
    if date_error:
        return date_error

    db.session.commit()

    insert_appointment_notifications(appointment, action_name="thay đổi")
    current_app.config["DISABLE_SIGNALS"] = False

    return "", "SUCCESS"


@handle_db_errors
def delete_appointment_service(current_user, appointment_id):
    if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
        return {"message": "Chỉ lễ tân được thực hiện"}, "FORBIDDEN"

    appointment = db.session.get(Appointment, int(appointment_id))
    if not appointment:
        return {"message": "Lịch hẹn không tồn tại"}, "NOT_FOUND"

    if appointment.status != StatusRole.CANCEL:
        return {"message": "Chỉ được phép xóa lịch hẹn ở trạng thái đã hủy"}, "ERROR_BAD_REQUEST"

    db.session.delete(appointment)
    db.session.commit()

    return "", "SUCCESS"


def validate_doctor(doctor):
    if not doctor or doctor.role.name != "DOCTOR" or not doctor.is_active:
        return {"message": "Bác sĩ không hợp lệ"}, "ERROR_BAD_REQUEST"

    return None, None


def validate_appointment_booking(doctor_id, str_appointment_date, get_time_slots):
    appointment_datetime, parsed_error = parse_appointment_datetime(str_appointment_date)

    if parsed_error:
        return None, None, parsed_error

    input_date_error, status = validate_appointment_date(appointment_datetime)

    if input_date_error:
        return None, None, (input_date_error, status)

    doctor = get_doctor_by_id(doctor_id)
    not_found_error, status = validate_doctor(doctor)

    if not_found_error:
        return None, None, (not_found_error, status)

    target_date = appointment_datetime.date()
    available_slots = get_time_slots(doctor, target_date)
    validate_error, status = validate_available_slot(appointment_datetime, available_slots)

    if validate_error:
        return None, None, (validate_error, status)

    return appointment_datetime, doctor, None


def get_or_create_patient(data):
    try:
        birthday_dt = datetime.strptime(data.get("birthday"), "%Y-%m-%d").date()
        gender_enum = GenderRole[data.get("gender").upper()]
    except (ValueError, KeyError, AttributeError):
        return None, ({"message": "Thông tin ngày sinh hoặc giới tính không hợp lệ"},
                      "ERROR_BAD_REQUEST")

    patient_profile = PatientProfile.query.join(User).filter(
        User.first_name == data.get("firstName"),
        User.last_name == data.get("lastName"),
        PatientProfile.phone == data.get("phone"),
        PatientProfile.gender == gender_enum,
        PatientProfile.birthday == birthday_dt,
        PatientProfile.address == data.get("address")
    ).first()

    if not patient_profile:
        unique_str = uuid.uuid4().hex[:8]
        new_user = User(
            username=f"pt{unique_str}",
            password=generate_password_hash(f"A1@a{unique_str}"),
            email=f"pt{unique_str}@clinic.com",
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            role=UserRole.PATIENT
        )
        db.session.add(new_user)
        db.session.flush()

        patient_profile = PatientProfile(
            user_id=new_user.id,
            phone=data.get("phone"),
            gender=gender_enum,
            birthday=birthday_dt,
            address=data.get("address"),
        )
        db.session.add(patient_profile)
        db.session.flush()

    return patient_profile, None


@handle_db_errors
def create_receptionist_appointment_service(current_user, data):
    if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
        return {"message": "Không có quyền thực hiện"}, "FORBIDDEN"

    appointment_date, doctor, error = validate_appointment_booking(
        data.get("doctorId"), data.get("appointmentDate"), get_available_time_slots
    )
    if error:
        return error

    patient_profile, patient_error = get_or_create_patient(data)
    if patient_error:
        return patient_error

    full_name = f"{data.get('lastName')} {data.get('firstName')}"
    new_appointment = Appointment(
        name=f"Khám bệnh - {full_name}",
        note=data.get("note", ""),
        status=StatusRole.APPROVED,
        appointment_date=appointment_date,
        doctor_profile_id=doctor.profile.id,
        patient_profile_id=patient_profile.id,
    )

    db.session.add(new_appointment)
    db.session.commit()

    return format_appointment(new_appointment, doctor, full_name), "SUCCESS"


def get_booked_appointments(doctor_id, target_date):
    return Appointment.query.filter(
        Appointment.doctor_profile_id == doctor_id,
        func.date(Appointment.appointment_date) == target_date,
        Appointment.status.in_([StatusRole.APPROVED, StatusRole.COMPLETED])
    ).all()


def get_available_time_slots(doctor, target_date):
    if not doctor.profile or doctor.profile.profile_type != "doctor":
        return []

    schedule = doctor.profile.work_schedule
    if not schedule:
        return []

    target_day_name = target_date.strftime('%A').upper()
    working_days = [work_schedule.day_of_week.name for work_schedule in schedule.work_dates]
    if target_day_name not in working_days:
        return []

    duration = get_slot_duration(doctor.profile)
    appointments = get_booked_appointments(doctor.profile.id, target_date)
    current_date = datetime.combine(target_date, schedule.start_time)
    end_date = datetime.combine(target_date, schedule.end_time)
    now_date = datetime.now()
    available = []

    while current_date + duration <= end_date:
        if current_date <= now_date:
            current_date += timedelta(minutes=30)
            continue

        if not check_is_conflicting(current_date, duration, appointments):
            available.append(current_date.isoformat() + "Z")

        current_date += timedelta(minutes=30)

    return available


@handle_db_errors
def get_time_slots_service(doctor_id, date_str):
    doctor = get_doctor_by_id(doctor_id)

    if not doctor or not doctor.profile:
        return {"message": "Bác sĩ không tồn tại"}, "NOT_FOUND"

    try:
        if date_str:
            target_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        else:
            target_date = date.today()
    except ValueError:
        return {"message": "Định dạng không hợp lệ (YYYY-MM-DD)"}, "ERROR_BAD_REQUEST"

    today = date.today()
    if target_date < today or target_date > (today + timedelta(days=7)):
        return {"message": "Chỉ xem được lịch trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"

    profile = doctor.profile
    work_schedule_data = None

    if profile.work_schedule:
        work_schedule = profile.work_schedule
        work_schedule_data = format_work_schedule(work_schedule)

    available_slots = get_available_time_slots(doctor, target_date)

    result = [
        {
            "workSchedule": work_schedule_data,
            "availableTimeSlots": available_slots,
        }
    ]
    return result, "SUCCESS"


@handle_db_errors
def create_medical_record_service(current_user, appointment_id, data):
    if current_user.role.name != "DOCTOR":
        return {"message": "Chỉ bác sĩ mới có quyền này"}, "FORBIDDEN"

    appointment = Appointment.query.get(int(appointment_id))
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

    db.session.add(record)
    db.session.flush()

    appointment.medical_record_id = record.id
    appointment.status = StatusRole.COMPLETED

    db.session.commit()

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
    if payload_status in ["DONE", "FOLLOW_UP"]:
        record.type = MedicalRecordType[payload_status]
        if record.appointment:
            record.appointment.status = StatusRole.COMPLETED

    db.session.commit()

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
