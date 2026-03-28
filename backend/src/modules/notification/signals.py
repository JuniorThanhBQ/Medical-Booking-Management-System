from sqlalchemy import event, select

from src.modules.appointments.models import Appointment
from src.modules.auth_profiles.models import DoctorProfile, PatientProfile
from src.modules.notification.models import Notification


def insert_notifications(connection, appointment, action: str):
    doctor_user_id = connection.scalar(
        select(DoctorProfile.user_id).where(
            DoctorProfile.id == appointment.doctor_profile_id
        )
    )

    patient_user_id = connection.scalar(
        select(PatientProfile.user_id).where(
            PatientProfile.id == appointment.patient_profile_id
        )
    )

    patient_notification = {
        "title": f"Lịch hẹn đã được {action}",
        "message": f"Lịch hẹn của bạn đã được {action} với Mã: {appointment.id}.",
        "is_read": False,
        "user_id": patient_user_id,
        "appointment_id": appointment.id
    }

    doctor_notification = {
        "title": f"Có cập nhật lịch hẹn: {action}",
        "message": f"Hệ thống vừa {action} một lịch hẹn có Mã: {appointment.id}.",
        "is_read": False,
        "user_id": doctor_user_id,
        "appointment_id": appointment.id
    }

    if doctor_user_id and patient_user_id:
        connection.execute(
            Notification.__table__.insert(),
            [patient_notification, doctor_notification]
        )


@event.listens_for(Appointment, 'after_insert')
def appointment_after_insert_listener(_mapper, connection, target):
    insert_notifications(connection, target, action="tạo mới")


@event.listens_for(Appointment, 'after_update')
def appointment_after_update_listener(_mapper, connection, target):
    insert_notifications(connection, target, action="cập nhật")
