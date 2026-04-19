from dependency_injector import containers, providers

from src.modules.appointments.containers import AppointmentContainer
from src.modules.doctors.containers import DoctorContainer
from src.modules.medical_records.containers import MedicalRecordContainer
from src.modules.notification.containers import NotificationContainer
from src.modules.users.containers import UserContainer


class AppContainer(containers.DeclarativeContainer):
    user_app = providers.Container(UserContainer)
    notification_app = providers.Container(NotificationContainer)
    doctor_app = providers.Container(DoctorContainer)
    appointment_app = providers.Container(
        AppointmentContainer,
        doctor_repository=doctor_app.repository,
        doctor_service=doctor_app.service
    )
    doctor_app.appointment_repository.override(appointment_app.repository)
    medical_record_app = providers.Container(
        MedicalRecordContainer,
        appointment_repository=appointment_app.repository
    )

    wiring_config = containers.WiringConfiguration(modules=[
        "src.modules.users.views",
        "src.modules.notification.views",
        "src.modules.notification.rabbitmq.signals",
        "src.modules.notification.rabbitmq.tasks",
        "src.modules.medical_records.views",
        "src.modules.doctors.views",
        "src.modules.appointments.views"
    ])
