from src.modules.appointments.views import (AppointmentListCreateAPI,
                                            AppointmentRetrieveUpdateDeleteAPI,
                                            PatientRetrieveAPI,
                                            ReceptionistAppointmentCreateAPI,
                                            appointments_namespace)

appointments_namespace.add_resource(AppointmentListCreateAPI, "")
appointments_namespace.add_resource(AppointmentRetrieveUpdateDeleteAPI, "/<int:appointment_id>")
appointments_namespace.add_resource(PatientRetrieveAPI, "/<int:appointment_id>/patient-profile")
appointments_namespace.add_resource(ReceptionistAppointmentCreateAPI, "/receptionist-appointments")
