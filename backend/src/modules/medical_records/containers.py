from dependency_injector import containers, providers

from src.modules.medical_records.repositories import MedicalRecordRepository
from src.modules.medical_records.services import MedicalRecordService


class MedicalRecordContainer(containers.DeclarativeContainer):
    appointment_repository = providers.Dependency()
    repository = providers.Singleton(MedicalRecordRepository)
    service = providers.Factory(
        MedicalRecordService,
        medical_record_repository=repository,
        appointment_repository=appointment_repository
    )
