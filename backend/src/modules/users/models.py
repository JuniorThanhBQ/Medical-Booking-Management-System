import datetime
from zoneinfo import ZoneInfo
import enum

from flask_login import UserMixin
from sqlalchemy import (Boolean, Column, Date, DateTime, Enum, ForeignKey,
                        Integer, String, Text)
from sqlalchemy.orm import backref, relationship

from src.extensions import db

VN_TZ = ZoneInfo("Asia/Ho_Chi_Minh")


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


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=lambda: datetime.datetime.now(VN_TZ).replace(tzinfo=None))    
    updated_date = Column(DateTime, 
                          default=lambda: datetime.datetime.now(VN_TZ).replace(tzinfo=None),
                          onupdate=lambda: datetime.datetime.now(VN_TZ).replace(tzinfo=None))


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

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "dateOfBirth": self.birthday.isoformat() if self.birthday else None,
            "phone": self.phone,
            "gender": self.gender.name if self.gender else None,
            "avatar": self.avatar,
            "profileType": self.profile_type
        }

    def update_from_dict(self, data):
        if "address" in data:
            self.address = data["address"]
        if "phone" in data:
            self.phone = data["phone"]


class PatientProfile(Profile):
    __tablename__ = "patient_profile"
    __mapper_args__ = {"polymorphic_identity": "patient"}
    id = Column(Integer,
                ForeignKey("profile.id", ondelete="CASCADE"),
                primary_key=True)
    medical_history = Column(Text)

    def to_dict(self):
        data = super().to_dict()
        data.update({
            "medicalHistory": self.medical_history
        })
        return data

    def update_from_dict(self, data):
        super().update_from_dict(data)
        if "medicalHistory" in data:
            self.medical_history = data["medicalHistory"]
