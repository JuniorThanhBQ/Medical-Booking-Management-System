from src.modules.appointments.views import (AppointmentListCreateAPI,
                                            AppointmentRetrieveUpdateDeleteAPI,
                                            CreateMedicalRecordAPI,
                                            MedicalRecordRetrieveUpdateAPI,
                                            PatientRetrieveAPI,
                                            PublicDoctorSlotListAPI,
                                            ReceptionistAppointmentCreateAPI,
                                            appointments_namespace,
                                            medical_records_namespace,
                                            public_namespace)

appointments_namespace.add_resource(AppointmentListCreateAPI, "")
appointments_namespace.add_resource(AppointmentRetrieveUpdateDeleteAPI, "/<int:appointment_id>")
appointments_namespace.add_resource(PatientRetrieveAPI, "/<int:appointment_id>/patient-profile")
appointments_namespace.add_resource(ReceptionistAppointmentCreateAPI, "/receptionist-appointments")
public_namespace.add_resource(PublicDoctorSlotListAPI, "/doctors/<int:doctor_id>/time-slots")
medical_records_namespace.add_resource(MedicalRecordRetrieveUpdateAPI, "/<int:medical_record_id>")
medical_records_namespace.add_resource(CreateMedicalRecordAPI, "/appointments/<int:appointment_id>")

