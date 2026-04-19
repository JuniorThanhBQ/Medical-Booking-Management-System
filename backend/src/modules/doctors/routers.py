from src.modules.doctors import doctors_namespace, public_namespace
from src.modules.doctors.views import (PublicDoctorListAPI,
                                       PublicDoctorRegisterAPI,
                                       PublicDoctorRetrieveAPI,
                                       PublicDoctorSlotListAPI,
                                       PublicMedicalServiceListAPI,
                                       PublicMedicalServiceRetrieveAPI,
                                       PublicSpecialtyListAPI,
                                       PublicSpecialtyRetrieveAPI,
                                       RetrieveMyScheduleAPI,
                                       ScheduleRequestAPI)

doctors_namespace.add_resource(RetrieveMyScheduleAPI, '/my-schedule')
doctors_namespace.add_resource(ScheduleRequestAPI, '/schedule-requests')
public_namespace.add_resource(PublicSpecialtyListAPI, "/specialties")
public_namespace.add_resource(PublicSpecialtyRetrieveAPI, "/specialties/<int:specialty_id>")
public_namespace.add_resource(PublicMedicalServiceListAPI, "/medical-services")
public_namespace.add_resource(PublicMedicalServiceRetrieveAPI, "/medical-services/<int:service_id>")
public_namespace.add_resource(PublicDoctorListAPI, "/doctors")
public_namespace.add_resource(PublicDoctorRetrieveAPI, "/doctors/<int:doctor_id>")
public_namespace.add_resource(PublicDoctorSlotListAPI, "/doctors/<int:doctor_id>/time-slots")
public_namespace.add_resource(PublicDoctorRegisterAPI, "/doctors-registration")
