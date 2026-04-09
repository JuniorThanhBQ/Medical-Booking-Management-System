import enum

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Text, Time
from sqlalchemy.orm import backref, relationship

from src.modules.users.models import Base, Profile


class DayOfWeek(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class WorkSchedule(Base):
    __tablename__ = "work_schedule"
    title = Column(String(255), nullable=False)
    description = Column(Text)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    work_dates = relationship(
        "WorkDate", backref="work_schedule", cascade="all, delete-orphan"
    )
    doctor_id = Column(Integer, ForeignKey("doctor_profile.id", ondelete="CASCADE"))

    def __str__(self):
        return self.title


class WorkDate(Base):
    __tablename__ = "work_dates"
    day_of_week = Column(Enum(DayOfWeek), nullable=False, index=True)
    work_schedule_id = Column(
        Integer, ForeignKey("work_schedule.id", ondelete="CASCADE"), nullable=False
    )

    def __str__(self):
        return self.day_of_week.name


class CtaLabel(enum.Enum):
    CK1 = 1
    CK2 = 2
    CK3 = 3


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
