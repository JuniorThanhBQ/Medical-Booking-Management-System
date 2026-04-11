from src.modules.users import auth_namespace
from src.modules.users.views import (EmailValidatorAPI, LoginAPI, RegisterAPI,
                                     RetrieveCurrentUserAPI)

auth_namespace.add_resource(LoginAPI, "/login")
auth_namespace.add_resource(RegisterAPI, "/register")
auth_namespace.add_resource(EmailValidatorAPI, "/email-validator")
auth_namespace.add_resource(RetrieveCurrentUserAPI, "/current-user")
