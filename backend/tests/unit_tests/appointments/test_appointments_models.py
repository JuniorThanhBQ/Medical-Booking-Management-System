from datetime import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from src.modules.appointments.models import Appointment, StatusRole
from tests.test_base import test_app, test_session


class TestStatusRoleEnum:
    def test_status_role_valid(self):
        assert StatusRole.COMPLETED.value == 1
        assert StatusRole.APPROVED.value == 2
        assert StatusRole.PENDING.value == 3
        assert StatusRole.CANCEL.value == 4

    def test_status_role_invalid(self):
        with pytest.raises(ValueError):
            StatusRole(99)


class TestAppointmentModel:
    def test_appointment_lifecycle(self, test_session):
        appointment_date = datetime(2025, 12, 1, 9, 0)
        appointment = Appointment(
            name="General Checkup",
            note="Patient feels tired",
            appointment_date=appointment_date,
            doctor_profile_id=1,
            patient_profile_id=2
        )
        test_session.add(appointment)
        test_session.commit()

        fetched_appointment = test_session.query(Appointment).filter_by(name="General Checkup").first()
        assert fetched_appointment is not None
        assert fetched_appointment.note == "Patient feels tired"

        fetched_appointment.note = "Patient feels better"
        test_session.commit()

        updated_appointment = test_session.query(Appointment).filter_by(name="General Checkup").first()
        assert updated_appointment.note == "Patient feels better"

        test_session.delete(updated_appointment)
        test_session.commit()

        deleted_appointment = test_session.query(Appointment).filter_by(name="General Checkup").first()
        assert deleted_appointment is None

    def test_appointment_missing_fields(self, test_session):
        appointment = Appointment(name="Incomplete Data")
        test_session.add(appointment)
        with pytest.raises(IntegrityError):
            test_session.commit()

    def test_appointment_default_status(self, test_session):
        appointment_date = datetime(2025, 12, 1, 10, 0)
        appointment = Appointment(
            name="Default Status Check",
            note="Testing status role",
            appointment_date=appointment_date,
            doctor_profile_id=1,
            patient_profile_id=2
        )
        test_session.add(appointment)
        test_session.commit()

        assert appointment.status == StatusRole.APPROVED

    def test_appointment_string_format(self):
        appointment_date = datetime(2025, 12, 1, 11, 0)
        appointment = Appointment(
            name="String Format Appointment",
            note="Testing string format",
            appointment_date=appointment_date,
            doctor_profile_id=1,
            patient_profile_id=2
        )
        assert str(appointment) == "String Format Appointment"

    def test_appointment_foreign_keys(self, test_session):
        appointment_date = datetime(2025, 12, 1, 14, 0)
        appointment = Appointment(
            name="Foreign Key Appointment",
            note="Testing foreign keys",
            appointment_date=appointment_date,
            doctor_profile_id=10,
            patient_profile_id=20,
            medical_record_id=30
        )
        test_session.add(appointment)
        test_session.commit()

        fetched_appointment = test_session.query(Appointment).filter_by(name="Foreign Key Appointment").first()
        assert fetched_appointment.doctor_profile_id == 10
        assert fetched_appointment.patient_profile_id == 20
        assert fetched_appointment.medical_record_id == 30

    def test_appointment_set_null_action(self, test_session):
        appointment_date = datetime(2025, 12, 1, 15, 0)
        appointment = Appointment(
            name="Null Action Appointment",
            note="Testing null on delete",
            appointment_date=appointment_date,
            doctor_profile_id=1,
            patient_profile_id=2,
            medical_record_id=100
        )
        test_session.add(appointment)
        test_session.commit()

        test_session.execute(
            Appointment.__table__.update().where(
                Appointment.id == appointment.id
            ).values(medical_record_id=None)
        )
        test_session.commit()

        fetched_appointment = test_session.query(Appointment).filter_by(name="Null Action Appointment").first()
        assert fetched_appointment.medical_record_id is None
