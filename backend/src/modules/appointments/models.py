import enum

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        UniqueConstraint)
from sqlalchemy.orm import backref, relationship

from src.modules.doctors.models import Base


class StatusRole(enum.Enum):
    COMPLETED = 1
    APPROVED = 2
    PENDING = 3
    CANCEL = 4
    SKIPPED = 5


class Appointment(Base):
    __tablename__ = "appointment"
    name = Column(String(100), nullable=False)
    note = Column(String(500), nullable=False)
    status = Column(Enum(StatusRole), default=StatusRole.APPROVED)
    appointment_date = Column(DateTime, nullable=False)
    doctor_profile_id = Column(Integer, ForeignKey("doctor_profile.id"), nullable=False)
    patient_profile_id = Column(Integer, ForeignKey("patient_profile.id"), nullable=False)
    medical_record_id = Column(
        Integer, ForeignKey("medical_record.id", ondelete="SET NULL"), nullable=True
    )
    medical_service_id = Column(
        Integer, ForeignKey("medical_services.id", ondelete="RESTRICT"), nullable=False
    )
    doctor = relationship("DoctorProfile", backref=backref("appointments"), lazy=True)
    patient = relationship("PatientProfile", backref=backref("appointments"), lazy=True)
    medical_record = relationship(
        "MedicalRecord",
        backref=backref("appointment", uselist=False),
        lazy=True
    )
    medical_service = relationship(
        "MedicalService",
        backref=backref("appointments"),
        lazy=True
    )

    def __str__(self):
        return self.name


class BookingLock(Base):
    __tablename__ = "booking_lock"

    doctor_name = Column(String(255), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    service_name = Column(String(255), nullable=True)

    __table_args__ = (
        UniqueConstraint('doctor_name', 'appointment_date', name='unique_doctor_time_lock'),
    )
