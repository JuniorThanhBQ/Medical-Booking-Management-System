from unittest.mock import patch

import pytest
from flask_restx import Api

from src.modules.appointments.views import medical_records_namespace
from src.modules.users.models import User, UserRole
from src.utils.utils import create_token
from tests.test_base import test_app, test_session


@pytest.fixture
def configured_client(test_app):
    if hasattr(medical_records_namespace, 'apis'):
        medical_records_namespace.apis.clear()

    api = Api(test_app)
    api.add_namespace(medical_records_namespace, path="/medical-records")
    return test_app.test_client()


@pytest.fixture
def doctor_user_view(test_session):
    user = User(
        username="doctor_view_test",
        password="hashed_password",
        email="doctor_view@test.com",
        first_name="Jane",
        last_name="Doe",
        is_active=True
    )
    user.role = UserRole.DOCTOR
    test_session.add(user)
    test_session.commit()
    return user


@pytest.fixture
def authorized_header(doctor_user_view, test_app):
    with test_app.app_context():
        token = create_token(doctor_user_view)
    return {"Authorization": f"Bearer {token}"}


class TestMedicalRecordRetrieveUpdateAPI:
    @patch("src.modules.medical_records.views.get_detail_medical_record_service")
    def test_get_record_success(self, mock_service, configured_client, authorized_header):
        mock_service.return_value = ({"id": "1", "diagnosis": "Flu"}, "SUCCESS")
        response = configured_client.get("/medical-records/1", headers=authorized_header)
        assert response.status_code == 200
        assert response.json["id"] == "1"

    @patch("src.modules.medical_records.views.get_detail_medical_record_service")
    def test_get_record_error(self, mock_service, configured_client, authorized_header):
        mock_service.return_value = ({"message": "Not Found"}, "NOT_FOUND")
        response = configured_client.get("/medical-records/999", headers=authorized_header)
        assert response.status_code == 404

    @patch("src.modules.medical_records.views.update_medical_record_service")
    def test_patch_record_success(self, mock_service, configured_client, authorized_header):
        mock_service.return_value = ({"id": 1}, "SUCCESS")
        payload = {"diagnosis": "Updated Cold"}
        response = configured_client.patch(
            "/medical-records/1", json=payload, headers=authorized_header
        )
        assert response.status_code == 200

    def test_patch_record_xss_violation(self, configured_client, authorized_header):
        payload = {"diagnosis": "<script>alert(1)</script>"}
        response = configured_client.patch(
            "/medical-records/1", json=payload, headers=authorized_header
        )
        assert response.status_code == 400
        assert "Dữ liệu đầu vào chứa ký tự không hợp lệ" in response.json["message"]
