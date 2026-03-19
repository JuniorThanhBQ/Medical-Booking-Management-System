from datetime import datetime
from enum import Enum

from flask_login import UserMixin
from sqlalchemy import Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship

from src import db

class StatusRole(Enum):
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
    updated_date = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())

class MedicalRecord(Base):
    __tablename__ = "medical_record"

    description = db.Column(db.String(500), nullable=False)