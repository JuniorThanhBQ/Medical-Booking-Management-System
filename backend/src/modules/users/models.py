from datetime import datetime
from enum import Enum

from flask_login import UserMixin
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src import db


class UserRole(Enum):
    PATIENT = 1
    DOCTOR = 2
    ADMINISTRATOR = 3


class GenderRole(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3


class Base(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False, default="")
    created_date = Column(DateTime, default=datetime.utcnow)

    def __str__(self):
        return self.name


class User(Base, UserMixin):
    __tablename__ = "user"

    address = Column(String(500))
    avatar = Column(
        String(500),
        default="https://shorturl.at/KNuMX",
    )

    birthday = Column(Date)
    email = Column(String(200), unique=True)
    gender = Column(Enum(GenderRole), default=GenderRole.OTHER)
    phone = Column(String(20))
    role = Column(Enum(UserRole), default=UserRole.PATIENT)

    password = Column(String(255), nullable=False)

    account = relationship("Account", backref="user", lazy=True, uselist=False)

    @property
    def is_patient(self):
        return self.role == UserRole.PATIENT

    @property
    def is_doctor(self):
        return self.role == UserRole.DOCTOR

    @property
    def is_administrator(self):
        return self.role == UserRole.ADMINISTRATOR
