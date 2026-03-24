from datetime import datetime
from unittest.mock import MagicMock, patch

from tests.test_base import test_app, test_session


class MockRole:
    def __init__(self, name):
        self.name = name


class MockSpecialty:
    def __init__(self, name="Cardiology"):
        self.id = 1
        self.name = name
        self.cta_label = MagicMock()
        self.cta_label.name = "CK1"


class MockUser:
    def __init__(self, role_name, profile_id=None, user_id=1, first_name="John", last_name="Doe"):
        self.id = user_id
        self.role = MockRole(role_name)
        self.first_name = first_name
        self.last_name = last_name
        self.profile = MagicMock(id=profile_id) if profile_id else None


class MockPatient:
    def __init__(self):
        self.user = MockUser("PATIENT", first_name="John", last_name="Doe")


class MockDoctor:
    def __init__(self):
        self.user = MockUser("DOCTOR", first_name="Jane", last_name="Smith")
        self.specialty = MockSpecialty()


class TestGetMedicalRecordDetail:
    @patch("flask_sqlalchemy.query.Query.get")
    def test_doctor_retrieves_their_patients_medical_record_successfully(self, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            get_detail_medical_record_service
        doctor_user = MockUser("DOCTOR", profile_id=1)
        mock_record = MagicMock()
        mock_record.id = 10
        mock_record.doctor_profile_id = 1
        mock_record.appointment.id = 50
        mock_record.appointment.status.name = "COMPLETED"
        mock_record.doctor = MockDoctor()
        mock_record.patient = MockPatient()
        mock_record.diagnosis = "Healthy"
        mock_record.note = "Routine checkup"
        mock_record.prescription_text = "None"
        mock_record.treatment_orders = "None"
        mock_record.created_date = datetime(2026, 3, 23)
        mock_record.updated_date = datetime(2026, 3, 23)
        mock_get.return_value = mock_record
        result, status = get_detail_medical_record_service(doctor_user, 10)
        assert status == "SUCCESS"
        assert result["id"] == "10"

    @patch("flask_sqlalchemy.query.Query.get")
    def test_patient_retrieves_their_own_medical_record_successfully(self, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            get_detail_medical_record_service
        patient_user = MockUser("PATIENT", profile_id=5)
        mock_record = MagicMock()
        mock_record.id = 10
        mock_record.patient_profile_id = 5
        mock_record.patient = MockPatient()
        mock_record.doctor = MockDoctor()
        mock_record.appointment = MagicMock()
        mock_get.return_value = mock_record
        result, status = get_detail_medical_record_service(patient_user, 10)
        assert status == "SUCCESS"
        assert result["id"] == "10"

    @patch("flask_sqlalchemy.query.Query.get")
    def test_access_denied_for_unauthorized_doctor(self, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            get_detail_medical_record_service
        doctor_user = MockUser("DOCTOR", profile_id=2)
        mock_record = MagicMock(doctor_profile_id=1)
        mock_get.return_value = mock_record
        result, status = get_detail_medical_record_service(doctor_user, 10)
        assert status == "FORBIDDEN"

    @patch("flask_sqlalchemy.query.Query.get")
    def test_access_denied_for_unauthorized_patient(self, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            get_detail_medical_record_service
        patient_user = MockUser("PATIENT", profile_id=6)
        mock_record = MagicMock(patient_profile_id=5)
        mock_get.return_value = mock_record
        result, status = get_detail_medical_record_service(patient_user, 10)
        assert status == "FORBIDDEN"

    @patch("flask_sqlalchemy.query.Query.get")
    def test_retrieve_non_existent_medical_record(self, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            get_detail_medical_record_service
        doctor_user = MockUser("DOCTOR")
        mock_get.return_value = None
        result, status = get_detail_medical_record_service(doctor_user, 999)
        assert status == "NOT_FOUND"


class TestCreateMedicalRecord:
    @patch("flask_sqlalchemy.query.Query.get")
    @patch("src.modules.medical_records.services.db.session.add")
    @patch("src.modules.medical_records.services.db.session.flush")
    @patch("src.modules.medical_records.services.db.session.commit")
    def test_doctor_creates_medical_record_successfully(self, mock_commit, mock_flush, mock_add, mock_get, test_app,
                                                        test_session):
        from src.modules.medical_records.services import \
            create_medical_record_service
        doctor_user = MockUser("DOCTOR", profile_id=1)
        mock_appointment = MagicMock(doctor_profile_id=1, medical_record=None)
        mock_get.return_value = mock_appointment
        data = {"status": "DONE", "diagnosis": "Flu"}
        result, status = create_medical_record_service(doctor_user, 50, data)
        assert status == "SUCCESS"
        mock_commit.assert_called_once()

    @patch("flask_sqlalchemy.query.Query.get")
    def test_prevent_duplicate_medical_records_for_single_appointment(self, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            create_medical_record_service
        doctor_user = MockUser("DOCTOR", profile_id=1)
        mock_appointment = MagicMock(doctor_profile_id=1, medical_record=MagicMock())
        mock_get.return_value = mock_appointment
        result, status = create_medical_record_service(doctor_user, 51, {"status": "DONE"})
        assert status == "BAD_REQUEST"

    @patch("flask_sqlalchemy.query.Query.get")
    def test_creation_fails_due_to_invalid_status_payload(self, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            create_medical_record_service
        doctor_user = MockUser("DOCTOR", profile_id=1)
        mock_appointment = MagicMock(doctor_profile_id=1, medical_record=None)
        mock_get.return_value = mock_appointment
        result, status = create_medical_record_service(doctor_user, 50, {"status": "INVALID"})
        assert status == "BAD_REQUEST"

    @patch("flask_sqlalchemy.query.Query.get")
    def test_access_denied_for_unauthorized_doctor(self, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            create_medical_record_service
        doctor_user = MockUser("DOCTOR", profile_id=2)
        mock_appointment = MagicMock(doctor_profile_id=1)
        mock_get.return_value = mock_appointment
        result, status = create_medical_record_service(doctor_user, 50, {"status": "DONE"})
        assert status == "FORBIDDEN"


class TestUpdateMedicalRecord:
    @patch("flask_sqlalchemy.query.Query.get")
    @patch("src.modules.medical_records.services.db.session.commit")
    def test_doctor_updates_medical_record_successfully(self, mock_commit, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            update_medical_record_service
        doctor_user = MockUser("DOCTOR", profile_id=1)
        mock_record = MagicMock(id=10, doctor_profile_id=1)
        mock_get.return_value = mock_record
        data = {"diagnosis": "Severe Flu", "status": "FOLLOW_UP"}
        result, status = update_medical_record_service(doctor_user, 10, data)
        assert status == "SUCCESS"
        mock_commit.assert_called_once()

    @patch("flask_sqlalchemy.query.Query.get")
    @patch("src.modules.medical_records.services.db.session.commit")
    def test_update_ignores_invalid_status_silently(self, mock_commit, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            update_medical_record_service
        doctor_user = MockUser("DOCTOR", profile_id=1)
        mock_record = MagicMock(id=10, doctor_profile_id=1)
        mock_get.return_value = mock_record
        result, status = update_medical_record_service(doctor_user, 10, {"status": "UNKNOWN"})
        assert status == "SUCCESS"

    @patch("flask_sqlalchemy.query.Query.get")
    def test_access_denied_for_unauthorized_doctor_updating_record(self, mock_get, test_app, test_session):
        from src.modules.medical_records.services import \
            update_medical_record_service
        doctor_user = MockUser("DOCTOR", profile_id=2)
        mock_record = MagicMock(id=10, doctor_profile_id=1)
        mock_get.return_value = mock_record
        result, status = update_medical_record_service(doctor_user, 10, {"diagnosis": "Test"})
        assert status == "FORBIDDEN"
