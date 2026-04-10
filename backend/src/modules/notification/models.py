import enum

from sqlalchemy import Boolean, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from src.modules.doctors.models import Base


class NotificationType(enum.Enum):
    SYSTEM = 1
    APPOINTMENT = 2
    PROMOTION = 3
    REMINDER = 4


class DeliveryStatus(enum.Enum):
    NONE = 0
    PENDING = 1
    SENT = 2
    FAILED = 3


class Notification(Base):
    __tablename__ = "notification"
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    type = Column(Enum(NotificationType), default=NotificationType.SYSTEM, index=True)
    send_email = Column(Boolean, default=False)
    email_status = Column(Enum(DeliveryStatus), default=DeliveryStatus.NONE)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", backref="notifications")
    appointment_id = Column(Integer, ForeignKey("appointment.id"))
    appointment = relationship("Appointment", backref="notifications")
