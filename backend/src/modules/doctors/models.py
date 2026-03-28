import enum

from sqlalchemy import (Column, DateTime, Enum, ForeignKey, Integer, String,
                        Text, Time, func)
from sqlalchemy.orm import relationship

from src.extensions import db


class DayOfWeek(enum.Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


class Base(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=func.now())  # pylint: disable=not-callable
    updated_date = Column(DateTime, default=func.now(), onupdate=func.now())  # pylint: disable=not-callable


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
