import enum
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import (Boolean, Column, Date, DateTime, Enum, ForeignKey,
                        Integer, String)
from sqlalchemy.orm import relationship

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


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.utcnow)


class User(Base, UserMixin):
    __tablename__ = "user"

    username = Column(String(100), unique=True, nullable=False, default="")
    password = Column(String(100), nullable=False, default="")
    first_name = Column(String(100), nullable=False, default="")
    last_name = Column(String(100), nullable=False, default="")
    email = Column(String(200), unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.PATIENT)
    is_active = Column(Boolean, default=True, nullable=False)


class Profile(db.Model):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, autoincrement=True)
    address = Column(String(100), nullable=False, default="")
    birthday = Column(DateTime, default=datetime.utcnow)
    phone = Column(String(100), nullable=False, default="")
    idenfication = Column(String(100), nullable=False, default="")
    avatar = Column(String(100), nullable=False, default="")
    updated_date = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("user.id"), nullable=False, unique=True)
    user = relationship("User", backref="profile")


class DoctorProfile(Profile):
    __tablename__ = "doctor_profile"

    id = Column(Integer, ForeignKey("profile.id"), primary_key=True)
    about = Column(String(100), nullable=False, default="")
    year_of_experience = Column(String(100), nullable=False, default="")


class PatientProfile(Profile):
    __tablename__ = "patient_profile"

    id = Column(Integer, ForeignKey("profile.id"), primary_key=True)
    medical_history = Column(String(100), nullable=False, default="")
