from datetime import date, datetime, timedelta
from unittest.mock import patch

from src.extensions import db
from src.modules.appointments.models import Appointment, StatusRole
from src.modules.doctors.models import DoctorProfile
from src.modules.notification.models import (DeliveryStatus, Notification,
                                             NotificationType)
from src.modules.notification.repositories import (
    add_and_commit_notification, bulk_mark_as_read, commit,
    delete_notification, get_appointments_for_date, get_by_id_and_user_id,
    get_doctor_user_info, get_existing_notification, get_notification_by_id,
    get_paginated_notification_by_user_id, get_patient_user_info,
    get_pending_email_notifications, get_unread_by_user_id,
    insert_notifications_list, rollback, update_email_status)
from src.modules.users.models import PatientProfile, User
from tests.test_base import test_app, test_client, test_session


@patch('src.modules.notification.rabbitmq.signals.reminder_email_task.apply_async')
def test_notification_repositories(test_app, test_session):
    with test_app.app_context():
        doc_user = User(username="doc", password="pwd", email="doc@test.com", first_name="D", last_name="C")
        pat_user = User(username="pat", password="pwd", email="pat@test.com", first_name="P", last_name="T")
        db.session.add_all([doc_user, pat_user])
        db.session.commit()

        dp = DoctorProfile(user_id=doc_user.id, title="ThS.BS", bio="Yolo", specialty_id=1)
        pp = PatientProfile(user_id=pat_user.id)
        db.session.add_all([dp, pp])
        db.session.commit()

        apt = Appointment(name="testmockappointment", note="Khamtest",medical_service_id=1,
            doctor_profile_id=dp.id, patient_profile_id=pp.id,
            appointment_date=datetime.now(), status=StatusRole.APPROVED
        )
        db.session.add(apt)
        db.session.commit()

        n1 = Notification(
            title="T1", message="M1", user_id=pat_user.id, appointment_id=apt.id,
            type=NotificationType.SYSTEM, send_email=True, email_status=DeliveryStatus.PENDING
        )
        add_and_commit_notification(n1)

        assert get_notification_by_id(n1.id).title == "T1"
        assert len(get_paginated_notification_by_user_id(pat_user.id, 1, 10).items) == 2
        assert len(get_unread_by_user_id(pat_user.id)) == 2
        assert get_by_id_and_user_id(n1.id, pat_user.id) is not None

        bulk_mark_as_read([n1])
        assert get_notification_by_id(n1.id).is_read is True

        update_email_status(n1, DeliveryStatus.SENT)
        assert get_notification_by_id(n1.id).email_status == DeliveryStatus.SENT

        assert len(get_appointments_for_date(date.today())) == 1
        assert get_existing_notification(apt.id, NotificationType.SYSTEM) is not None
        assert get_doctor_user_info(dp.id).email == "doc@test.com"
        assert get_patient_user_info(pp.id).email == "pat@test.com"

        n1.email_status = DeliveryStatus.PENDING
        n1.created_date = datetime.now() - timedelta(minutes=20)
        db.session.commit()

        with db.engine.connect() as conn:
            notifs = [{
                "title": "T2", "message": "M2", "user_id": doc_user.id, "appointment_id": apt.id,
                "type": NotificationType.APPOINTMENT, "is_read": False, "send_email": False,
                "email_status": DeliveryStatus.SENT
            }]
            ids = insert_notifications_list(notifs, conn)
            conn.commit()
            assert len(ids) == 1

        delete_notification(n1)
        assert get_notification_by_id(n1.id) is None

        n2 = Notification(title="T3", message="M3", user_id=pat_user.id)
        db.session.add(n2)
        commit()
        assert get_notification_by_id(n2.id) is not None

        n3 = Notification(title="T4", message="M4", user_id=pat_user.id)
        db.session.add(n3)
        rollback()