import logging
from datetime import datetime, timedelta

from src.modules.notification.models import (DeliveryStatus, Notification,
                                             NotificationType)

logger = logging.getLogger(__name__)


class NotificationAPIService:
    def __init__(self, notification_repository):
        self.notification_repository = notification_repository

    def get_notifications_service(self, current_user, page=1, per_page=10):
        paginated_data = self.notification_repository.get_paginated_notification_by_user_id(
            current_user.id, page, per_page)

        data = {
            "items": [
                {
                    "id": n.id,
                    "title": n.title,
                    "message": n.message,
                    "is_read": n.is_read,
                    "type": n.type.name if n.type else "SYSTEM",
                    "created_at": n.created_date.isoformat() + "Z" if n.created_date else None,
                } for n in paginated_data.items
            ],
            "meta": {
                "page": paginated_data.page,
                "per_page": paginated_data.per_page,
                "total_pages": paginated_data.pages,
                "total_items": paginated_data.total,
                "has_next": paginated_data.has_next,
                "has_prev": paginated_data.has_prev
            }
        }

        return data, "SUCCESS"

    def get_detail_notification_service(self, current_user, notification_id):
        notification = self.notification_repository.get_by_id_and_user_id(
            notification_id, current_user.id)
        if not notification:
            return None, "NOT_FOUND"

        result = {
            "id": notification.id,
            "title": notification.title,
            "message": notification.message,
            "is_read": notification.is_read,
            "type": notification.type.name if notification.type else "SYSTEM",
            "created_at": notification.created_date.isoformat() + "Z"
            if notification.created_date else None,
            "appointment_id": notification.appointment_id,
            "send_email": notification.send_email,
        }
        return result, "SUCCESS"

    def mark_all_notification_service(self, current_user):
        unread_notifies = self.notification_repository.get_unread_by_user_id(current_user.id)
        if unread_notifies:
            self.notification_repository.bulk_mark_as_read(unread_notifies)

        return "", "SUCCESS"

    def mark_detail_notification_service(self, current_user, notification_id):
        notification = self.notification_repository.get_by_id_and_user_id(
            notification_id, current_user.id)
        if not notification:
            return None, "NOT_FOUND"

        if not notification.is_read:
            notification.is_read = True
            self.notification_repository.commit()

        return "", "SUCCESS"

    def delete_notification_service(self, current_user, notification_id):
        notification = self.notification_repository.get_by_id_and_user_id(
            notification_id, current_user.id)
        if not notification:
            return None, "NOT_FOUND"

        self.notification_repository.delete_notification(notification)
        return "", "SUCCESS"

    def insert_appointment_notifications(self, appointment=None, connection=None, action_name=None):
        doctor = self.notification_repository.get_doctor_user_info(appointment.doctor_profile_id)
        patient = self.notification_repository.get_patient_user_info(appointment.patient_profile_id)

        if doctor and patient and connection is not None:
            doctor_name = f"{doctor.last_name} {doctor.first_name}"
            patient_name = f"{patient.last_name} {patient.first_name}"

            created_notifications = [
                {
                    "title": f"Lịch hẹn {appointment.name} đã được {action_name}",
                    "message": f"Chào {patient_name}, lịch hẹn của bạn với BS. {doctor_name} đã được {action_name}.",
                    "user_id": patient.id,
                    "appointment_id": appointment.id,
                    "type": NotificationType.APPOINTMENT,
                    "is_read": False,
                    "send_email": True,
                    "email_status": DeliveryStatus.PENDING
                },
                {
                    "title": f"Thông báo {action_name} trong lịch hẹn {appointment.name}",
                    "message": f"Chào BS. {doctor_name}, lịch hẹn của bệnh nhân {patient_name} "
                               f"do bạn phụ trách vừa được {action_name}.",
                    "user_id": doctor.id,
                    "appointment_id": appointment.id,
                    "type": NotificationType.APPOINTMENT,
                    "is_read": False,
                    "send_email": True,
                    "email_status": DeliveryStatus.PENDING
                }
            ]

            try:
                notification_list = self.notification_repository.insert_notifications_list(
                    created_notifications, connection)
                return notification_list
            except Exception as e:
                self.notification_repository.rollback()
                raise e

        return None


class NotificationTaskService:
    def __init__(self, notification_repository):
        self.notification_repository = notification_repository

    def generate_daily_reminders_service(self):
        tomorrow = datetime.now().date() + timedelta(days=1)
        upcoming_appointments = self.notification_repository.get_appointments_for_date(tomorrow)

        if not upcoming_appointments:
            logger.info(f"Không có lịch hẹn cho ({tomorrow}).")
            return []

        notifications_to_send = []
        count = 0

        for appointment in upcoming_appointments:
            existing_notification = self.notification_repository.get_existing_notification(
                appointment_id=appointment.id,
                notif_type=NotificationType.REMINDER
            )

            if not existing_notification:
                appointment_time = appointment.appointment_date.strftime("%H:%M")
                date_str = tomorrow.strftime('%d/%m/%Y')

                doctor = self.notification_repository.get_doctor_user_info(appointment.doctor_profile_id)
                patient = self.notification_repository.get_patient_user_info(appointment.patient_profile_id)

                if patient:
                    patient_name = f"{patient.last_name} {patient.first_name}"
                    doctor_name = f"{doctor.last_name} {doctor.first_name}" if doctor else "Bác sĩ"

                    p_notif = Notification(
                        title="Nhắc nhở: Lịch hẹn khám bệnh ngày mai",
                        message=(f"Xin chào {patient_name}, bạn có lịch khám với BS. {doctor_name} "
                                 f"vào lúc {appointment_time} ngày mai ({date_str}) tại 97 Võ Văn Tần."),
                        type=NotificationType.REMINDER,
                        send_email=True,
                        email_status=DeliveryStatus.PENDING,
                        user_id=patient.id,
                        appointment_id=appointment.id
                    )
                    self.notification_repository.add_and_commit_notification(p_notif)
                    notifications_to_send.append(p_notif.id)
                    count += 1

                if doctor:
                    patient_name = f"{patient.last_name} {patient.first_name}" if patient else "Khách hàng"
                    d_notif = Notification(
                        title="Nhắc nhở: Lịch làm việc ngày mai",
                        message=(f"Xin chào BS. {doctor.last_name} {doctor.first_name}, Bác sĩ có lịch khám "
                                 f"cho bệnh nhân {patient_name} vào lúc {appointment_time} ngày mai ({date_str})."),
                        type=NotificationType.REMINDER,
                        send_email=True,
                        email_status=DeliveryStatus.PENDING,
                        user_id=doctor.id,
                        appointment_id=appointment.id
                    )
                    self.notification_repository.add_and_commit_notification(d_notif)
                    notifications_to_send.append(d_notif.id)
                    count += 1

        logger.info(f"Tổng cộng: {count} thông báo nhắc lịch trong ngày.")
        return notifications_to_send

    def get_pending_emails_service(self):
        notifications = self.notification_repository.get_pending_email_notifications()
        return [n.id for n in notifications] if notifications else []
