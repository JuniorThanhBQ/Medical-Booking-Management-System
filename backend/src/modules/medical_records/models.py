import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, Text
from sqlalchemy.orm import backref, relationship

from src.modules.doctor.models import Base


class MedicalRecordType(enum.Enum):
    DONE = 1
    FOLLOW_UP = 2


class MedicalRecord(Base):
    __tablename__ = "medical_record"
    note = Column(Text)
    type = Column(Enum(MedicalRecordType), default=MedicalRecordType.DONE)
    diagnosis = Column(Text, nullable=False)
    prescription_text = Column(Text, nullable=False)
    treatment_orders = Column(Text, nullable=False)
    doctor_profile_id = Column(Integer, ForeignKey("doctor_profile.id"), nullable=False)
    patient_profile_id = Column(Integer, ForeignKey("patient_profile.id"), nullable=False)
    doctor = relationship("DoctorProfile", backref=backref("medical_records"), lazy=True)
    patient = relationship("PatientProfile", backref=backref("medical_records"), lazy=True)

    def __str__(self):
        return f"Phiếu điều trị: {self.patient_profile_id} - {self.diagnosis}"
