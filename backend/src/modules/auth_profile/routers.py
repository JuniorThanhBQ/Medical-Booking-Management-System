from flask import Blueprint
from flask_restful import Api

from src.modules.auth_profile.views import (EmailValidatorAPI, GoogleLoginAPI,
                                            LoginAPI, RegisterAPI,
                                            RetrieveCurrentUserAPI)

auth_profile_blueprint = Blueprint("auth_profile", __name__)
api = Api(auth_profile_blueprint)

api.add_resource(LoginAPI, "/login")
api.add_resource(RegisterAPI, "/register")
api.add_resource(EmailValidatorAPI, "/email-validator")
api.add_resource(GoogleLoginAPI, "/google-login")
api.add_resource(RetrieveCurrentUserAPI, "/current-user")
