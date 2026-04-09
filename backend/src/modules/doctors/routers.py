from src.modules.doctors.views import (PublicDoctorListAPI,
                                       PublicDoctorRetrieveAPI,
                                       PublicSpecialtyListAPI,
                                       PublicSpecialtyRetrieveAPI,
                                       RetrieveMyScheduleAPI,
                                       ScheduleRequestAPI, doctors_namespace,
                                       public_namespace)

doctors_namespace.add_resource(RetrieveMyScheduleAPI, '/my-schedule')
doctors_namespace.add_resource(ScheduleRequestAPI, '/schedule-requests')
public_namespace.add_resource(PublicSpecialtyListAPI, "/specialties")
public_namespace.add_resource(PublicSpecialtyRetrieveAPI, "/specialties/<int:specialty_id>")
public_namespace.add_resource(PublicDoctorListAPI, "/doctors")
public_namespace.add_resource(PublicDoctorRetrieveAPI, "/doctors/<int:doctor_id>")