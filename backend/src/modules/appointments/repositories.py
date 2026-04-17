import uuid
from datetime import datetime, time, timedelta

from werkzeug.security import generate_password_hash

from src.extensions import db
from src.modules.appointments.models import Appointment, BookingLock
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

def clean_expired_booking_locks(minutes=20):
    expiration_time = datetime.utcnow() - timedelta(minutes=minutes)
    BookingLock.query.filter(BookingLock.created_date < expiration_time).delete()
    db.session.flush()

def get_active_booking_lock(doctor_name, appointment_date):
    return BookingLock.query.filter_by(
        doctor_name=doctor_name,
        appointment_date=appointment_date
    ).first()

def create_booking_lock(doctor_name, appointment_date, service_name):
    new_lock = BookingLock(
        doctor_name=doctor_name,
        appointment_date=appointment_date,
        service_name=service_name
    )
    db.session.add(new_lock)
    db.session.flush()
    return new_lock

def delete_booking_lock(doctor_name, appointment_date):
    lock = BookingLock.query.filter_by(
        doctor_name=doctor_name,
        appointment_date=appointment_date
    ).first()
    if lock:
        db.session.delete(lock)
        db.session.flush()

def get_locked_time_slots(doctor_name, target_date):
    expiration_time = datetime.now() - timedelta(minutes=20)
    start_of_day = datetime.combine(target_date, time.min)
    end_of_day = datetime.combine(target_date, time.max)
    locks = BookingLock.query.filter(
        BookingLock.doctor_name == doctor_name,
        BookingLock.appointment_date >= start_of_day,
        BookingLock.appointment_date <= end_of_day,
        BookingLock.created_date >= expiration_time
    ).all()

    return [lock.appointment_date for lock in locks]
