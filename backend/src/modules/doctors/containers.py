from dependency_injector import containers, providers

from src.modules.doctors.repositories import DoctorRepository
from src.modules.doctors.services import DoctorService


class DoctorContainer(containers.DeclarativeContainer):
    appointment_repository = providers.Dependency()
    repository = providers.Singleton(DoctorRepository)
    service = providers.Factory(
        DoctorService,
        doctor_repository=repository,
        appointment_repository=appointment_repository
    )
