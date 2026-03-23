from flask import request
from flask_restful import Resource

from src.modules.public.services import (get_doctor_detail_service,
                                         get_doctors_service,
                                         get_specialties_service,
                                         get_specialty_detail_service,
                                         get_time_slots_service)
from src.utils.utils import format_api_response


class PublicSpecialtyListAPI(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("limit", 10, type=int)
        keywords = request.args.get("keywords", type=str)
        cta_label = request.args.get("ctaLabel", type=str)

        data, message = get_specialties_service(
            page=page, per_page=per_page, keywords=keywords, cta_label=cta_label
        )

        return {
            "message": message,
            "data": data
        }, 200


class PublicSpecialtyRetrieveAPI(Resource):
    def get(self, specialty_id):
        return format_api_response(*get_specialty_detail_service(specialty_id))


class PublicDoctorListAPI(Resource):
    def get(self):
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("limit", 10, type=int)
        keywords = request.args.get("keywords", type=str)
        specialty_id = request.args.get("specialtyId", type=int)

        data, message = get_doctors_service(
            page=page, per_page=per_page, keywords=keywords, specialty_id=specialty_id
        )

        return {
            "message": message,
            "data": data
        }, 200


class PublicDoctorRetrieveAPI(Resource):
    def get(self, doctor_id):
        return format_api_response(*get_doctor_detail_service(doctor_id))


class PublicDoctorSlotListAPI(Resource):
    def get(self, doctor_id):
        date_str = request.args.get("date")
        return format_api_response(*get_time_slots_service(doctor_id, date_str))
