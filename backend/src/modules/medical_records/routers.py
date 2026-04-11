from src.modules.medical_records import medical_records_namespace
from src.modules.medical_records.views import (CreateMedicalRecordAPI,
                                               MedicalRecordListAPI,
                                               MedicalRecordRetrieveUpdateAPI,
                                               )

medical_records_namespace.add_resource(MedicalRecordListAPI, "")
medical_records_namespace.add_resource(MedicalRecordRetrieveUpdateAPI, "/<int:medical_record_id>")
medical_records_namespace.add_resource(CreateMedicalRecordAPI, "/appointments/<int:appointment_id>")
