from unittest.mock import patch

import pytest
from flask_restx import Api

from src.modules.doctors.views import doctors_namespace
from src.modules.users.models import User, UserRole
from src.utils.utils import create_token
from tests.test_base import test_app, test_session


@pytest.fixture
def configured_client(test_app):
    if hasattr(doctors_namespace, 'apis'):
        doctors_namespace.apis.clear()

    api = Api(test_app)
    api.add_namespace(doctors_namespace, path="/doctors")
    return test_app.test_client()


@pytest.fixture
def doctor_user_fixture(test_session):
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
def authorized_header(doctor_user_fixture, test_app):
    with test_app.app_context():
        token = create_token(doctor_user_fixture)
    return {"Authorization": f"Bearer {token}"}


class TestRetrieveMyScheduleAPI:
    @patch("src.modules.doctors.views.get_my_schedule_service")
    def test_get_schedule_success(self, mock_service, configured_client, authorized_header):
        mock_service.return_value = ({"workSchedule": {}, "appointments": []}, "SUCCESS")
        response = configured_client.get("/doctors/my-schedule", headers=authorized_header)
        assert response.status_code == 200
        assert "workSchedule" in response.json

    @patch("src.modules.doctors.views.get_my_schedule_service")
    def test_get_schedule_forbidden_error(self, mock_service, configured_client, authorized_header):
        mock_service.return_value = ({"message": "Forbidden"}, "FORBIDDEN")
        response = configured_client.get("/doctors/my-schedule", headers=authorized_header)
        assert response.status_code == 403


class TestScheduleRequestAPI:
    @patch("src.modules.doctors.views.request_schedule_change_service")
    def test_post_change_request_success(self, mock_service, configured_client, authorized_header):
        mock_service.return_value = ({"id": 1}, "SUCCESS")
        payload = {
            "newWorkSchedule": {
                "title": "New Shift",
                "start_time": "08:00:00",
                "end_time": "12:00:00",
                "work_date": ["MONDAY"]
            }
        }
        response = configured_client.post("/doctors/schedule-requests", json=payload,
                                          headers=authorized_header)
        assert response.status_code == 201

    def test_post_request_xss_violation(self, configured_client, authorized_header):
        payload = {
            "newWorkSchedule": {
                "title": "Shift",
                "start_time": "08:00:00",
                "end_time": "12:00:00"
            },
            "reason": "<script>alert('xss')</script>"
        }
        response = configured_client.post("/doctors/schedule-requests", json=payload,
                                          headers=authorized_header)
        assert response.status_code == 400
        assert response.json["message"] == "Dữ liệu đầu vào chứa ký tự không hợp lệ"

    @patch("src.modules.doctors.views.request_schedule_change_service")
    def test_post_change_request_error(self, mock_service, configured_client, authorized_header):
        mock_service.return_value = ({"message": "Bad Request"}, "ERROR_BAD_REQUEST")
        payload = {"newWorkSchedule": {"start_time": "08:00:00", "end_time": "12:00:00"}}
        response = configured_client.post("/doctors/schedule-requests", json=payload,
                                          headers=authorized_header)
        assert response.status_code == 400
