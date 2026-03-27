from src.modules.public.views import (PublicDoctorListAPI,
                                      PublicDoctorRetrieveAPI,
                                      PublicDoctorSlotListAPI,
                                      PublicSpecialtyListAPI,
                                      PublicSpecialtyRetrieveAPI,
                                      public_namespace)

public_namespace.add_resource(PublicSpecialtyListAPI, "/specialties")
public_namespace.add_resource(PublicSpecialtyRetrieveAPI, "/specialties/<int:specialty_id>")
public_namespace.add_resource(PublicDoctorListAPI, "/doctors")
public_namespace.add_resource(PublicDoctorRetrieveAPI, "/doctors/<int:doctor_id>")
public_namespace.add_resource(PublicDoctorSlotListAPI, "/doctors/<int:doctor_id>/time-slots")
