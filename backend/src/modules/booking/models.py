import enum
from datetime import datetime

from sqlalchemy import (Boolean, Column, Date, DateTime, Enum, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship
from src import db
from src.modules.users.models import DoctorProfile, PatientProfile


class StatusRole(enum.Enum):
    COMPLETED = 1
    APPROVED = 2
    PENDING = 3
    CANCEL = 4


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.now())


class Appointment(Base):
    __tablename__ = "appointment"

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    status = db.Column(Enum(StatusRole), default=StatusRole.APPROVED)
    updated_date = db.Column(
        db.DateTime, default=datetime.now(), onupdate=datetime.now()
    )

    doctorprofile_id = Column(Integer, ForeignKey("doctor_profile.id"), nullable=False)
    doctor = relationship("DoctorProfile", backref="appointment")

    patientprofile_id = Column(
        Integer, ForeignKey("patient_profile.id"), nullable=False
    )
    patient = relationship("PatientProfile", backref="appointment")

    medicalrecord_id = Column(Integer, ForeignKey("medical_record.id"), nullable=True)
    medicalrecord = relationship("MedicalRecord", backref="appointment")


class MedicalRecord(Base):
    __tablename__ = "medical_record"

    description = db.Column(db.String(500), nullable=False)
