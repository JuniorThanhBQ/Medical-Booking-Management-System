import enum

from flask_login import UserMixin
from sqlalchemy import (Boolean, Column, Date, Enum, ForeignKey, Integer,
                        String, Text)
from sqlalchemy.orm import backref, relationship

from src.modules.doctors.models import Base


class UserRole(enum.Enum):
    DOCTOR = 1
    RECEPTIONIST = 2
    PATIENT = 3
    ADMIN = 4


class GenderRole(enum.Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3
    NOT_SET = 4


class CtaLabel(enum.Enum):
    CK1 = 1
    CK2 = 2
    CK3 = 3


class User(Base, UserMixin):
    __tablename__ = "user"
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PATIENT, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Profile(Base):
    __tablename__ = "profile"
    profile_type = Column(String(100))
    __mapper_args__ = {"polymorphic_identity": "profile", "polymorphic_on": profile_type}
    address = Column(String(500))
    birthday = Column(Date)
    phone = Column(String(20))
    avatar = Column(String(500))
    gender = Column(Enum(GenderRole), default=GenderRole.NOT_SET, index=True)
    user_id = Column(Integer,
                     ForeignKey("user.id", ondelete="CASCADE"),
                     nullable=False,
                     unique=True)
    user = relationship(
        "User",
        backref=backref("profile", uselist=False, cascade="all, delete-orphan")
    )

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Specialty(Base):
    __tablename__ = "specialty"
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    level = Column(String(255), nullable=False)
    cta_label = Column(Enum(CtaLabel), default=CtaLabel.CK1)

    def __str__(self):
        return self.name


class DoctorProfile(Profile):
    __tablename__ = "doctor_profile"
    __mapper_args__ = {"polymorphic_identity": "doctor"}
    id = Column(Integer,
                ForeignKey("profile.id", ondelete="CASCADE"),
                primary_key=True)
    title = Column(String(255), nullable=False)
    bio = Column(Text, nullable=False)
    specialty_id = Column(Integer,
                          ForeignKey("specialty.id", ondelete="RESTRICT"),
                          nullable=False)
    specialty = relationship("Specialty", backref="doctors", lazy="joined")
    work_schedule = relationship(
        "WorkSchedule",
        backref=backref("doctor", uselist=False),
        uselist=False,
        cascade="all, delete-orphan",
        single_parent=True,
    )


class PatientProfile(Profile):
    __tablename__ = "patient_profile"
    __mapper_args__ = {"polymorphic_identity": "patient"}
    id = Column(Integer,
                ForeignKey("profile.id", ondelete="CASCADE"),
                primary_key=True)
    medical_history = Column(Text)


class AuditLog(Base):
    __tablename__ = "audit_log"
    action_name = Column(String(500), nullable=False)
    description = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    user = relationship("User", backref="audit_log")
