import uuid
from datetime import date, datetime, timedelta

from werkzeug.security import generate_password_hash

from src.extensions import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.auth_profile.models import (GenderRole, PatientProfile, User,
                                             UserRole)
from src.modules.public.services import get_available_time_slots
from src.utils.decorator import handle_db_errors


@handle_db_errors(parameter=2)
def get_appointments_list_service(current_user):
    role_name = current_user.role.name
    query = Appointment.query

    if role_name == "PATIENT":
        if not current_user.profile:
            return [], "SUCCESS"
        query = query.filter(Appointment.patient_profile_id == current_user.profile.id)
    elif role_name == "DOCTOR":
        if not current_user.profile:
            return [], "SUCCESS"
        query = query.filter(Appointment.doctor_profile_id == current_user.profile.id)
    elif role_name in ["RECEPTIONIST", "ADMIN"]:
        pass
    else:
        return {"message": "Không có quyền truy cập"}, "FORBIDDEN"

    appointments = query.order_by(Appointment.appointment_date.desc()).all()
    result = []

    for appointment in appointments:
        doctor_user = appointment.doctor.user
        patient_user = appointment.patient.user
        result.append(
            {
                "id": str(appointment.id),
                "patientName": f"{patient_user.last_name} {patient_user.first_name}",
                "doctorName": f"{doctor_user.last_name} {doctor_user.first_name}",
                "status": appointment.status.name if appointment.status else None,
                "appointmentDate": (
                    appointment.appointment_date.isoformat() + "Z"
                ),
            }
        )

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

    result = {
        "id": str(appointment.id),
        "type": specialty.cta_label.name if specialty and specialty.cta_label else None,
        "patientName": f"{patient_user.last_name} {patient_user.first_name}",
        "doctorName": f"{doctor_user.last_name} {doctor_user.first_name}",
        "appointmentDate":
            appointment.appointment_date.isoformat() + "Z",
        "status": appointment.status.name if appointment.status else None,
        "note": appointment.note,
        "createdAt": appointment.created_date.isoformat() + "Z" ,
        "updatedAt": appointment.updated_date.isoformat() + "Z" ,
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

    try:
        appointment_dt = (
            datetime.strptime(appointment_date_str.replace("Z", "").split(".")[0],
                              "%Y-%m-%dT%H:%M:%S")
        )
    except ValueError:
        return {"message": "Định dạng ngày không hợp lệ"}, "ERROR_BAD_REQUEST"

    target_date = appointment_dt.date()
    today = date.today()
    if target_date < today or target_date > today + timedelta(days=7):
        return {"message": "Chỉ được đặt lịch trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"

    doctor = db.session.get(User, int(doctor_id))
    if not doctor or doctor.role.name != "DOCTOR" or not doctor.is_active:
        return {"message": "Bác sĩ không hợp lệ"}, "ERROR_BAD_REQUEST"

    available_slots = get_available_time_slots(doctor, target_date)
    exact_iso = appointment_dt.isoformat() + "Z"
    if exact_iso not in available_slots:
        return {"message": "Khung giờ này không khả dụng hoặc đã có người đặt"}, "ERROR_BAD_REQUEST"

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

    return {
        "id": str(new_appointment.id),
        "type": doctor.profile.specialty.cta_label.name,
        "patientName": f"{current_user.last_name} {current_user.first_name}",
        "doctorName": f"{doctor.last_name} {doctor.first_name}",
        "appointmentDate": new_appointment.appointment_date.isoformat() + "Z",
        "status": new_appointment.status.name,
        "note": new_appointment.note,
        "createdAt": new_appointment.created_date.isoformat() + "Z",
        "updatedAt": new_appointment.updated_date.isoformat() + "Z"
    }, "SUCCESS"

@handle_db_errors(parameter=2)
# pylint: disable=too-many-return-statements
def create_receptionist_appointment_service(current_user, data):
    if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
        return {"message": "Không có quyền thực hiện"}, "FORBIDDEN"

    doctor_id = data.get("doctorId")
    appointment_date_str = data.get("appointmentDate")
    note = data.get("note", "")

    try:
        appointment_dt = (
            datetime.strptime(appointment_date_str.replace("Z", "").split(".")[0],
                              "%Y-%m-%dT%H:%M:%S")
        )
    except ValueError:
        return {"message": "Định dạng ngày không hợp lệ"}, "ERROR_BAD_REQUEST"

    target_date = appointment_dt.date()
    today = date.today()
    if target_date < today or target_date > today + timedelta(days=7):
        return {"message": "Chỉ được đặt lịch trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"

    doctor = db.session.get(User, int(doctor_id))
    if not doctor or doctor.role.name != "DOCTOR" or not doctor.is_active:
        return {"message": "Bác sĩ không hợp lệ"}, "ERROR_BAD_REQUEST"

    available_slots = get_available_time_slots(doctor, target_date)
    exact_iso = appointment_dt.isoformat() + "Z"
    if exact_iso not in available_slots:
        return {"message": "Khung giờ này không khả dụng hoặc đã có người đặt"}, "ERROR_BAD_REQUEST"

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

    return {
        "id": str(new_appointment.id),
        "type": doctor.profile.specialty.cta_label.name,
        "patientName": f"{last_name} {first_name}",
        "doctorName": f"{doctor.last_name} {doctor.first_name}",
        "appointmentDate": new_appointment.appointment_date.isoformat() + "Z",
        "status": new_appointment.status.name,
        "note": new_appointment.note,
        "createdAt": new_appointment.created_date.isoformat() + "Z",
        "updatedAt": new_appointment.updated_date.isoformat() + "Z"
    }, "SUCCESS"

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
        try:
            appointment_dt = datetime.strptime(appointment_date_str.replace("Z", "").split(".")[0],
                                               "%Y-%m-%dT%H:%M:%S")
        except ValueError:
            return {"message": "Định dạng ngày không hợp lệ"}, "ERROR_BAD_REQUEST"

        target_date = appointment_dt.date()
        today = date.today()
        if target_date < today or target_date > today + timedelta(days=7):
            return {"message": "Chỉ được đặt lịch trong vòng 7 ngày tới"}, "ERROR_BAD_REQUEST"

        if appointment.appointment_date != appointment_dt:
            doctor = appointment.doctor.user
            available_slots = get_available_time_slots(doctor, target_date)
            exact_iso = appointment_dt.isoformat() + "Z"

            if exact_iso not in available_slots:
                return {"message": "Khung giờ này không khả dụng"}, "ERROR_BAD_REQUEST"
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
