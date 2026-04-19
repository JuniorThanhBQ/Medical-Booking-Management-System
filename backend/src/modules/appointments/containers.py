from dependency_injector import containers, providers

from src.modules.appointments.repositories import AppointmentRepository
from src.modules.appointments.services import AppointmentService


class AppointmentContainer(containers.DeclarativeContainer):
    doctor_repository = providers.Dependency()
    doctor_service = providers.Dependency()
    repository = providers.Singleton(AppointmentRepository)
    service = providers.Factory(
        AppointmentService,
        appointment_repository=repository,
        doctor_repository=doctor_repository,
        doctor_service=doctor_service
    )
