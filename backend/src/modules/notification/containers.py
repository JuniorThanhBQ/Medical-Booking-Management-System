from dependency_injector import containers, providers

from src.modules.notification.repositories import NotificationRepository
from src.modules.notification.services import (NotificationAPIService,
                                               NotificationTaskService)


class NotificationContainer(containers.DeclarativeContainer):
    repository = providers.Singleton(NotificationRepository)
    notification_services = providers.Factory(NotificationAPIService, notification_repository=repository)
    mail_services = providers.Factory(NotificationTaskService, notification_repository=repository)
