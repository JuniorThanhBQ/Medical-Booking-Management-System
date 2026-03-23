import uuid
from datetime import datetime

from werkzeug.security import generate_password_hash

from src.extensions import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.auth_profile.models import (GenderRole, PatientProfile, User,
                                             UserRole)
from src.modules.public.services import get_available_time_slots
from src.utils.decorator import handle_db_errors
from src.utils.utils import (format_appointment_response,
                             validate_appointment_booking)


@handle_db_errors(parameter=2)
# pylint: disable=too-many-return-statements
def create_receptionist_appointment_service(current_user, data):
    if current_user.role.name not in ["RECEPTIONIST", "ADMIN"]:
        return {"message": "Không có quyền thực hiện"}, "FORBIDDEN"

    doctor_id = data.get("doctorId")
    appointment_date_str = data.get("appointmentDate")
    note = data.get("note", "")

    appointment_dt, doctor, error = validate_appointment_booking(
        doctor_id, appointment_date_str, get_available_time_slots, db.session
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
