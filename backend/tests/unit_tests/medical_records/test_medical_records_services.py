from datetime import datetime

import pytest

from src.modules.appointments.models import (Appointment, MedicalRecord,
                                             StatusRole)
from src.modules.appointments.services import (
    create_medical_record_service, get_detail_medical_record_service,
    update_medical_record_service)
from src.modules.doctors.models import DoctorProfile, Specialty
from src.modules.users.models import PatientProfile, User, UserRole
from tests.test_base import test_app, test_session


@pytest.fixture
def service_doctor_user(test_session):
    user = User(
        username="doctor_service_test",
        password="hashed_password",
        email="doctor_service@test.com",
        first_name="Jane",
        last_name="Doe",
        is_active=True
    )
    user.role = UserRole.DOCTOR
    test_session.add(user)
    test_session.flush()

    specialty = Specialty(name="Cardiology", level="1")
    test_session.add(specialty)
    test_session.flush()

    profile = DoctorProfile(title="Good doctor", bio="Good",
                            user_id=user.id, specialty_id=specialty.id)
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def service_patient_user(test_session):
    user = User(
        username="patient_service_test",
        password="hashed_password",
        email="patient_service@test.com",
        first_name="John",
        last_name="Smith",
        is_active=True
    )
    user.role = UserRole.PATIENT
    test_session.add(user)
    test_session.flush()

    profile = PatientProfile(user_id=user.id)
    test_session.add(profile)
    test_session.commit()
    return user


@pytest.fixture
def service_appointment_setup(test_session, service_doctor_user, service_patient_user):
    appointment = Appointment(
        name="General Checkup",
        note="I'm  Gendery",
        appointment_date=datetime.now(),
        doctor_profile_id=service_doctor_user.profile.id,
        patient_profile_id=service_patient_user.profile.id,
        status=StatusRole.APPROVED
    )
    test_session.add(appointment)
    test_session.commit()
    return appointment


@pytest.fixture
def service_medical_record(test_session, service_appointment_setup):
    record = MedicalRecord(
        diagnosis="Initial Diagnosis",
        prescription_text="Aspirin",
        treatment_orders="Rest",
        doctor_profile_id=service_appointment_setup.doctor_profile_id,
        patient_profile_id=service_appointment_setup.patient_profile_id
    )
    test_session.add(record)
    test_session.commit()
    service_appointment_setup.medical_record_id = record.id
    test_session.commit()
    return record


class TestGetDetailMedicalRecordService:
    def test_get_record_not_found(self, test_app, service_doctor_user):
        with test_app.app_context():
            result, status = get_detail_medical_record_service(service_doctor_user, 9999)
            assert status == "NOT_FOUND"

    def test_get_record_patient_forbidden(self, test_app, test_session, service_medical_record):
        other_patient = User(username="other_p", role=UserRole.PATIENT, password="1",
                             email="p@t.com", first_name="A",
                             last_name="B")
        test_session.add(other_patient)
        test_session.flush()
        other_profile = PatientProfile(user_id=other_patient.id)
        test_session.add(other_profile)
        test_session.commit()

        with test_app.app_context():
            result, status = get_detail_medical_record_service(other_patient, service_medical_record.id)
            assert status == "FORBIDDEN"

    def test_get_record_doctor_forbidden(self, test_app, test_session, service_medical_record):
        other_doctor = User(username="other_d", role=UserRole.DOCTOR, password="1",
                            email="d@t.com", first_name="C",
                            last_name="D")
        test_session.add(other_doctor)
        test_session.flush()
        other_profile = DoctorProfile(user_id=other_doctor.id, title="test",
                                      bio="test", specialty_id=1)
        test_session.add(other_profile)
        test_session.commit()

        with test_app.app_context():
            result, status = get_detail_medical_record_service(other_doctor,
                                                               service_medical_record.id)
            assert status == "FORBIDDEN"

    def test_get_medical_record_success(self, test_app, service_doctor_user, service_medical_record):
        with test_app.app_context():
            result, status = get_detail_medical_record_service(service_doctor_user,
                                                               service_medical_record.id)
            assert status == "SUCCESS"
            assert result["diagnosis"] == "Initial Diagnosis"
            assert "appointmentId" in result


class TestCreateMedicalRecordService:
    def test_create_record_not_doctor(self, test_app, service_patient_user):
        with test_app.app_context():
            result, status = create_medical_record_service(service_patient_user,
                                                           1, {})
            assert status == "FORBIDDEN"

    def test_create_appointment_not_found(self, test_app, service_doctor_user):
        with test_app.app_context():
            result, status = create_medical_record_service(service_doctor_user,
                                                           9999, {})
            assert status == "NOT_FOUND"

    def test_create_record_doctor_forbidden(self, test_app, test_session, service_appointment_setup):
        other_doctor = User(username="other_doc", role=UserRole.DOCTOR, password="1",
                            email="doc@t.com", first_name="X",
                            last_name="Y")
        test_session.add(other_doctor)
        test_session.flush()
        other_profile = DoctorProfile(user_id=other_doctor.id, title="test",
                                      bio="test", specialty_id=1)
        test_session.add(other_profile)
        test_session.commit()

        with test_app.app_context():
            result, status = create_medical_record_service(other_doctor,
                                                           service_appointment_setup.id, {})
            assert status == "FORBIDDEN"

    def test_create_record_already_exists(self, test_app, service_doctor_user, service_appointment_setup,
                                          service_medical_record):
        with test_app.app_context():
            result, status = create_medical_record_service(service_doctor_user,
                                                           service_appointment_setup.id, {})
            assert status == "BAD_REQUEST"

    def test_create_record_invalid_status(self, test_app, service_doctor_user, service_appointment_setup):
        data = {"status": "INVALID"}
        service_appointment_setup.medical_record_id = None
        with test_app.app_context():
            result, status = create_medical_record_service(service_doctor_user,
                                                           service_appointment_setup.id, data)
            assert status == "BAD_REQUEST"

    def test_create_medical_record_success(self, test_app, service_doctor_user,
                                           service_appointment_setup):
        data = {
            "status": "DONE",
            "diagnosis": "New Diagnosis",
            "prescriptionText": "Pills",
            "treatmentOrders": "Walk",
            "notes": "Good"
        }
        service_appointment_setup.medical_record_id = None
        with test_app.app_context():
            result, status = create_medical_record_service(service_doctor_user,
                                                           service_appointment_setup.id, data)
            assert status == "SUCCESS"
            assert result["diagnosis"] == "New Diagnosis"


class TestUpdateMedicalRecordService:
    def test_update_record_not_doctor(self, test_app, service_patient_user):
        with test_app.app_context():
            result, status = update_medical_record_service(service_patient_user,
                                                           1, {})
            assert status == "FORBIDDEN"

    def test_update_record_not_found(self, test_app, service_doctor_user):
        with test_app.app_context():
            result, status = update_medical_record_service(service_doctor_user,
                                                           9999, {})
            assert status == "NOT_FOUND"

    def test_update_record_doctor_forbidden(self, test_app, test_session, service_medical_record):
        other_doctor = User(username="bad_doc", role=UserRole.DOCTOR, password="1",
                            email="b@d.com", first_name="A",
                            last_name="B")
        test_session.add(other_doctor)
        test_session.flush()
        other_profile = DoctorProfile(user_id=other_doctor.id, title="test",
                                      bio="test", specialty_id=1)
        test_session.add(other_profile)
        test_session.commit()

        with test_app.app_context():
            result, status = update_medical_record_service(other_doctor,
                                                           service_medical_record.id, {})
            assert status == "FORBIDDEN"

    def test_update_medical_record_success(self, test_app, service_doctor_user, service_medical_record):
        data = {
            "diagnosis": "Updated Diagnosis",
            "notes": "Updated Notes",
            "status": "FOLLOW_UP"
        }
        with test_app.app_context():
            result, status = update_medical_record_service(service_doctor_user,
                                                           service_medical_record.id, data)
            assert status == "SUCCESS"
            assert result["diagnosis"] == "Updated Diagnosis"
            assert result["status"] == "FOLLOW_UP"
