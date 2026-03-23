from flask import Blueprint
from flask_restful import Api

from src.modules.appointments.views import (AppointmentListCreateAPI,
                                            AppointmentRetrieveUpdateDeleteAPI,
                                            PatientRetrieveAPI,
                                            ReceptionistAppointmentCreateAPI)

appointments_blueprint = Blueprint("appointments", __name__)
api = Api(appointments_blueprint)
api.add_resource(AppointmentListCreateAPI, "")
api.add_resource(AppointmentRetrieveUpdateDeleteAPI, "/<int:appointment_id>")
api.add_resource(PatientRetrieveAPI, "/<int:appointment_id>/patient-profile")
api.add_resource(ReceptionistAppointmentCreateAPI, "/receptionist-appointments")
