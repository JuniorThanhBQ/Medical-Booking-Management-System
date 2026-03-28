from src.modules.medical_records.views import (CreateMedicalRecordAPI,
                                               MedicalRecordRetrieveUpdateAPI,
                                               medical_records_namespace)

medical_records_namespace.add_resource(MedicalRecordRetrieveUpdateAPI, "/<int:medical_record_id>")
medical_records_namespace.add_resource(CreateMedicalRecordAPI, "/appointments/<int:appointment_id>")
