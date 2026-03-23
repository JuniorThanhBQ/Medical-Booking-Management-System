from flask import Blueprint
from flask_restful import Api

from src.modules.public.views import (PublicDoctorListAPI,
                                      PublicDoctorRetrieveAPI,
                                      PublicDoctorSlotListAPI,
                                      PublicSpecialtyListAPI,
                                      PublicSpecialtyRetrieveAPI)

public_blueprint = Blueprint("public", __name__)
api = Api(public_blueprint)

api.add_resource(PublicSpecialtyListAPI, "/specialties")
api.add_resource(PublicSpecialtyRetrieveAPI, "/specialties/<int:specialty_id>")
api.add_resource(PublicDoctorListAPI, "/doctors")
api.add_resource(PublicDoctorRetrieveAPI, "/doctors/<int:doctor_id>")
api.add_resource(PublicDoctorSlotListAPI, "/doctors/<int:doctor_id>/time-slots")
