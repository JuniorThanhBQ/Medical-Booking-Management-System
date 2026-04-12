import uuid

from werkzeug.security import generate_password_hash

from src.extensions import db
from src.modules.appointments.models import Appointment
from src.modules.users.models import PatientProfile, User, UserRole


def get_appointments_base_query():
    return Appointment.query


def get_appointment_by_id(appointment_id):
    return db.session.get(Appointment, int(appointment_id))


def get_patient_profile_by_details(first_name, last_name, phone, gender, birthday, address):
    return PatientProfile.query.join(User).filter(
        User.first_name == first_name,
        User.last_name == last_name,
        PatientProfile.phone == phone,
        PatientProfile.gender == gender,
        PatientProfile.birthday == birthday,
        PatientProfile.address == address
    ).first()


def create_new_patient_profile(first_name, last_name, phone, gender, birthday, address):
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
        gender=gender,
        birthday=birthday,
        address=address,
    )
    db.session.add(patient_profile)
    db.session.flush()
    return patient_profile


def add_instance(instance):
    db.session.add(instance)


def flush_session():
    db.session.flush()


def commit_session():
    db.session.commit()


def delete_instance(instance):
    db.session.delete(instance)
