from src.modules.appointments.views import (AppointmentListCreateAPI,
                                            AppointmentRetrieveUpdateDeleteAPI,
                                            PatientRetrieveAPI,
                                            ReceptionistAppointmentCreateAPI,
                                            TransactionLockAPI,
                                            TransactionUnlockAPI,
                                            appointments_namespace)

appointments_namespace.add_resource(AppointmentListCreateAPI, "")
appointments_namespace.add_resource(AppointmentRetrieveUpdateDeleteAPI, "/<int:appointment_id>")
appointments_namespace.add_resource(PatientRetrieveAPI, "/<int:appointment_id>/patient-profile")
appointments_namespace.add_resource(ReceptionistAppointmentCreateAPI, "/receptionist-appointments")
appointments_namespace.add_resource(TransactionLockAPI, "/transaction-locked")
appointments_namespace.add_resource(TransactionUnlockAPI, "/transaction-unlocked")
