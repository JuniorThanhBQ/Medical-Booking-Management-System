from flask import request
from flask_restful import Resource

from src.modules.public.services import (get_doctor_detail_service,
                                         get_doctors_service,
                                         get_specialties_service,
                                         get_time_slots_service)
from src.utils.utils import format_api_response


class PublicSpecialtyListAPI(Resource):
    def get(self):
        return format_api_response(*get_specialties_service())


class PublicDoctorListAPI(Resource):
    def get(self):
        return format_api_response(*get_doctors_service())


class PublicDoctorRetrieveAPI(Resource):
    def get(self, doctor_id):
        return format_api_response(*get_doctor_detail_service(doctor_id))


class PublicDoctorSlotListAPI(Resource):
    def get(self, doctor_id):
        date_str = request.args.get("date")
        return format_api_response(*get_time_slots_service(doctor_id, date_str))
