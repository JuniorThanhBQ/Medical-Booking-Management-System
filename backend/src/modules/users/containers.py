from dependency_injector import containers, providers

from src.modules.users.repositories import UserRepository
from src.modules.users.services import AuthService, UserService


class UserContainer(containers.DeclarativeContainer):
    repository = providers.Singleton(UserRepository)
    auth_service = providers.Factory(AuthService, user_repository=repository)
    profile_service = providers.Factory(UserService, user_repository=repository)
