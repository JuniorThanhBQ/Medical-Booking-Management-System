import uuid
from datetime import date, datetime, timedelta

from sqlalchemy import func
from werkzeug.security import generate_password_hash

from src.extensions import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.auth_profile.models import (GenderRole, PatientProfile, User,
                                             UserRole)
from src.utils.exception_decorator import handle_db_errors
from src.utils.utils import (format_appointment_response,
                             format_appointment_summary)


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
        "medicalRecordId": str(appointment.medical_record_id),
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
        doctor_id, appointment_date_str, get_available_time_slots
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


def parse_appointment_datetime(str_appointment_date):
    try:
        appointment_datetime = datetime.strptime(
            str_appointment_date.replace("Z", "").split(".")[0],
            "%Y-%m-%dT%H:%M:%S"
        )

        return appointment_datetime, None

    except ValueError:
        return None, ({"message": "Định dạng ngày không hợp lệ"}, "ERROR_BAD_REQUEST")


def validate_appointment_date(appointment_datetime):
    target_date = appointment_datetime.date()
    today = date.today()

    if target_date < today or target_date > (today + timedelta(days=7)):
        return {"message": "Chỉ được đặt lịch trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"

    return None, None


def validate_doctor(doctor):
    if not doctor or doctor.role.name != "DOCTOR" or not doctor.is_active:
        return {"message": "Bác sĩ không hợp lệ"}, "ERROR_BAD_REQUEST"

    return None, None


def validate_available_slot(appointment_datetime, available_slots):
    exact_iso = appointment_datetime.isoformat() + "Z"

    if exact_iso not in available_slots:
        return {"message": "Khung giờ này không khả dụng hoặc đã có người đặt"}, "ERROR_BAD_REQUEST"

    return None, None


def validate_appointment_booking(doctor_id, str_appointment_date, get_time_slots):
    appointment_datetime, parsed_error = parse_appointment_datetime(str_appointment_date)

    if parsed_error:
        return None, None, parsed_error

    input_date_error, status = validate_appointment_date(appointment_datetime)

    if input_date_error:
        return None, None, (input_date_error, status)

    doctor = User.query.get(int(doctor_id))
    not_found_error, status = validate_doctor(doctor)

    if not_found_error:
        return None, None, (not_found_error, status)

    target_date = appointment_datetime.date()
    available_slots = get_time_slots(doctor, target_date)
    validate_error, status = validate_available_slot(appointment_datetime, available_slots)

    if validate_error:
        return None, None, (validate_error, status)

    return appointment_datetime, doctor, None


@handle_db_errors(parameter=2)
# pylint: disable=too-many-return-statements
def create_receptionist_appointment_service(current_user, data):
    if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
        return {"message": "Không có quyền thực hiện"}, "FORBIDDEN"

    doctor_id = data.get("doctorId")
    appointment_date_str = data.get("appointmentDate")
    note = data.get("note", "")

    appointment_dt, doctor, error = validate_appointment_booking(
        doctor_id, appointment_date_str, get_available_time_slots
    )
    if error:
        if isinstance(error, tuple):
            return error
        return error

    first_name = data.get("firstName")
    last_name = data.get("lastName")
    phone = data.get("phone")
    gender = data.get("gender")
    birthday_str = data.get("birthday")
    address = data.get("address")

    try:
        birthday_dt = datetime.strptime(birthday_str, "%Y-%m-%d").date()
    except ValueError:
        return {"message": "Định dạng ngày sinh không hợp lệ"}, "ERROR_BAD_REQUEST"

    try:
        gender_enum = GenderRole[gender.upper()]
    except KeyError:
        return {"message": "Giới tính không hợp lệ"}, "ERROR_BAD_REQUEST"

    patient_profile = PatientProfile.query.join(User).filter(
        User.first_name == first_name,
        User.last_name == last_name,
        PatientProfile.phone == phone,
        PatientProfile.gender == gender_enum,
        PatientProfile.birthday == birthday_dt,
        PatientProfile.address == address
    ).first()

    if not patient_profile:
        unique_str = uuid.uuid4().hex[:8]
        new_user = User(
            username=f"pt{unique_str}",
            password=generate_password_hash(f"A1@a{unique_str}"),
            email=f"pt{unique_str}@clinic.com",
            first_name=first_name,
            last_name=last_name,
            role=UserRole.PATIENT
        )
        db.session.add(new_user)
        db.session.flush()

        patient_profile = PatientProfile(
            user_id=new_user.id,
            phone=phone,
            gender=gender_enum,
            birthday=birthday_dt,
            address=address,
        )
        db.session.add(patient_profile)
        db.session.flush()

    new_appointment = Appointment(
        name=f"Khám bệnh - {last_name} {first_name}",
        note=note,
        status=StatusRole.APPROVED,
        appointment_date=appointment_dt,
        doctor_profile_id=doctor.profile.id,
        patient_profile_id=patient_profile.id,
    )
    db.session.add(new_appointment)
    db.session.commit()

    response = format_appointment_response(new_appointment, doctor, f"{last_name} {first_name}")
    return response, "SUCCESS"


def get_available_time_slots(doctor, target_date):
    if not doctor.profile or doctor.profile.profile_type != "doctor":
        return []

    schedule = doctor.profile.work_schedule
    if not schedule:
        return []

    target_day_name = target_date.strftime('%A').upper()
    if not any(wd.day_of_week.name == target_day_name for wd in schedule.work_dates):
        return []

    if doctor.profile.specialty and doctor.profile.specialty.cta_label:
        specialty_cta = doctor.profile.specialty.cta_label.name
    else:
        specialty_cta = "CK1"

    hours = 1
    if specialty_cta == "CK2":
        hours = 2
    elif specialty_cta == "CK3":
        hours = 3
    duration = timedelta(hours=hours)

    appointments = Appointment.query.filter(
        Appointment.doctor_profile_id == doctor.profile.id,
        func.date(Appointment.appointment_date) == target_date,
        Appointment.status.in_([StatusRole.APPROVED, StatusRole.COMPLETED])
    ).all()

    available = []
    curr_dt = datetime.combine(target_date, schedule.start_time)
    end_dt = datetime.combine(target_date, schedule.end_time)
    now_dt = datetime.now()

    while curr_dt + duration <= end_dt:
        if curr_dt <= now_dt:
            curr_dt += timedelta(minutes=30)
            continue

        conflict = False
        for a in appointments:
            a_start = a.appointment_date
            a_end = a_start + duration
            if ((curr_dt + duration + timedelta(minutes=30) > a_start)
                    and (a_end + timedelta(minutes=30) > curr_dt)):
                conflict = True
                break

        if not conflict:
            available.append(curr_dt.isoformat() + "Z")

        curr_dt += timedelta(minutes=30)

    return available
