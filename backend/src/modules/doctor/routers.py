from flask import Blueprint
from flask_restful import Api

from src.modules.doctor.views import RetrieveMyScheduleAPI, ScheduleRequestAPI

doctors_blueprint = Blueprint("doctors", __name__)
api = Api(doctors_blueprint)

api.add_resource(RetrieveMyScheduleAPI, '/my-schedule')
api.add_resource(ScheduleRequestAPI, '/schedule-requests')
