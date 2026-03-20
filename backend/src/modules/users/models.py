import enum

from flask_login import UserMixin
from sqlalchemy import (Boolean, Column, Date, DateTime, Enum, ForeignKey,
                        Integer, String, Text, Time, func)
from sqlalchemy.orm import backref, relationship

from src import db


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


class SlotStatus(enum.Enum):
    LOCKER = 1
    OCCUPIED = 2
    AVAILABLE = 3


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=func.now())
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())


class User(Base, UserMixin):
    __tablename__ = "user"

    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PATIENT, index=True)
    is_active = Column(Boolean, nullable=False, default=True, index=True)

    def __str__(self):
        return self.username


class Profile(Base):
    __tablename__ = "profile"

    profile_type = Column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "profile",
        "polymorphic_on": profile_type,
    }

    address = Column(String(500))
    birthday = Column(DateTime)
    phone = Column(String(100))
    gender = Column(Enum(GenderRole), default=GenderRole.NOT_SET, index=True)
    avatar = Column(String(100))
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    user = relationship("User", backref=backref("profile", uselist=False))

    def __str__(self):
        return f"{self.user.last_name} {self.user.first_name}"


class Specialty(Base):
    __tablename__ = "specialty"

    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    image = Column(String(500))

    def __str__(self):
        return self.name


class WorkSchedule(Base):
    __tablename__ = "work_schedule"

    title = Column(String(255), nullable=False)
    description = Column(Text)

    def __str__(self):
        return self.title


class TimeSlot(Base):
    __tablename__ = "time_slot"

    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    date_slot = Column(Date, nullable=False)
    status = Column(Enum(SlotStatus), default=SlotStatus.AVAILABLE)
    work_schedule_id = Column(Integer, ForeignKey("work_schedule.id"), nullable=False)

    work_schedule = relationship("WorkSchedule", backref="time_slots")

    def __str__(self):
        return f"{self.work_schedule.title} - {self.date_slot}"


class DoctorProfile(Profile):
    __tablename__ = "doctor_profile"

    __mapper_args__ = {
        "polymorphic_identity": "doctor",
    }

    id = Column(Integer, ForeignKey("profile.id"), primary_key=True)
    about = Column(Text, nullable=False)
    year_of_experience = Column(Integer, nullable=False)
    specialty_id = Column(Integer, ForeignKey("specialty.id"), nullable=False)
    work_schedule_id = Column(Integer, ForeignKey("work_schedule.id"), nullable=False)
    specialty = relationship("Specialty", backref="doctors")
    work_schedule = relationship(
        "WorkSchedule", backref=backref("doctor", uselist=False)
    )


class PatientProfile(Profile):
    __tablename__ = "patient_profile"

    __mapper_args__ = {
        "polymorphic_identity": "patient",
    }

    id = Column(Integer, ForeignKey("profile.id"), primary_key=True)
    medical_history = Column(String(255))
