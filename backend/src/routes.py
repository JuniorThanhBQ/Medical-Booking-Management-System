from flask import Blueprint
from flask_restful import Api

from src.modules.appointments.views import (AppointmentListCreateAPI,
                                            AppointmentRetrieveUpdateAPI,
                                            PatientRetrieveAPI,
                                            ReceptionistAppointmentCreateAPI)
from src.modules.auth_profile.views import (GoogleLoginAPI, LoginAPI,
                                            RegisterAPI,
                                            RetrieveCurrentUserAPI)
from src.modules.doctor.views import RetrieveMyScheduleAPI, ScheduleRequestAPI
from src.modules.medical_records.views import (CreateMedicalRecordAPI,
                                               MedicalRecordRetrieveUpdateAPI)
from src.modules.notification.views import NotificationAPI
from src.modules.public.views import (PublicDoctorListAPI,
                                      PublicDoctorRetrieveAPI,
                                      PublicDoctorSlotListAPI,
                                      PublicSpecialtyListAPI)

api_v1 = Blueprint("auth_v1", __name__, url_prefix="/api/v1")
api = Api(api_v1)

api.add_resource(LoginAPI, "/auth/login")
api.add_resource(RegisterAPI, "/auth/register")
api.add_resource(GoogleLoginAPI, "/auth/google-login")
api.add_resource(RetrieveCurrentUserAPI, "/auth/current-user")

api.add_resource(PublicSpecialtyListAPI, "/public/specialties")
api.add_resource(PublicDoctorListAPI, "/public/doctors")
api.add_resource(PublicDoctorRetrieveAPI, "/public/doctors/<int:doctor_id>")
api.add_resource(PublicDoctorSlotListAPI, "/public/doctors/<int:doctor_id>/time-slots")

api.add_resource(AppointmentListCreateAPI, "/appointments")
api.add_resource(AppointmentRetrieveUpdateAPI, "/appointments/<int:appointment_id>")
api.add_resource(CreateMedicalRecordAPI, "/appointments/<int:appointment_id>/medical-record")
api.add_resource(PatientRetrieveAPI, "/appointments/<int:appointment_id>/patient-profile")

api.add_resource(RetrieveMyScheduleAPI, '/my-schedule')
api.add_resource(ScheduleRequestAPI, '/schedule-requests')
api.add_resource(MedicalRecordRetrieveUpdateAPI, "/medical-records/<int:medical_record_id>")

api.add_resource(ReceptionistAppointmentCreateAPI, "receptionist/appointments")
api.add_resource(NotificationAPI, '/notifications')
