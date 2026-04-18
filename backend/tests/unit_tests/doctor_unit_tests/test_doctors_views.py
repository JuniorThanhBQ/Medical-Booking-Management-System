from unittest.mock import patch

import pytest
from werkzeug.security import generate_password_hash

from src.modules.users.models import User, UserRole
from src.modules.users.repositories import add_user, commit
from src.utils.users.jwt_utils import create_token
from tests.test_base import test_app, test_client, test_session


@pytest.fixture
def auth_client(test_app, test_client):
    with test_app.app_context():
        user = User(
            username="doc_view", password=generate_password_hash("Pass@123"),
            email="docview@test.com", first_name="Doc", last_name="View", role=UserRole.DOCTOR
        )
        add_user(user)
        commit()
        token = create_token(user)

    test_client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"
    return test_client


@patch('src.modules.doctors.views.get_my_schedule_service', return_value=({}, "SUCCESS"))
def test_retrieve_my_schedule_api(mock_svc, auth_client):
    res = auth_client.get('/api/v1/doctors/my-schedule')
    assert res.status_code == 200


@patch('src.modules.doctors.views.request_schedule_change_service', return_value=({}, "SUCCESS"))
def test_schedule_request_api(mock_svc, auth_client):
    res = auth_client.post('/api/v1/doctors/schedule-requests', json={"reason": "<script>"})
    assert res.status_code == 400

    res = auth_client.post('/api/v1/doctors/schedule-requests', json={
        "newWorkSchedule": {"start_time": "08:00:00", "end_time": "17:00:00"}
    })
    assert res.status_code == 201


@patch('src.modules.doctors.views.get_specialties_service', return_value=([], "SUCCESS"))
def test_public_specialties_api(mock_svc, test_client):
    res = test_client.get('/api/v1/public/specialties?keywords=abc')
    assert res.status_code == 200


@patch('src.modules.doctors.views.get_specialty_detail_service', return_value=({}, "SUCCESS"))
def test_public_specialty_detail_api(mock_svc, test_client):
    res = test_client.get('/api/v1/public/specialties/1')
    assert res.status_code == 200


@patch('src.modules.doctors.views.get_medical_services_service', return_value=([], "SUCCESS"))
def test_public_medical_services_api(mock_svc, test_client):
    res = test_client.get('/api/v1/public/medical-services?specialtyId=1')
    assert res.status_code == 200


@patch('src.modules.doctors.views.get_medical_service_detail_service', return_value=({}, "SUCCESS"))
def test_public_medical_service_detail_api(mock_svc, test_client):
    res = test_client.get('/api/v1/public/medical-services/1')
    assert res.status_code == 200


@patch('src.modules.doctors.views.get_doctors_service', return_value=([], "SUCCESS"))
def test_public_doctors_api(mock_svc, test_client):
    res = test_client.get('/api/v1/public/doctors?keywords=bs&workDates=1')
    assert res.status_code == 200


@patch('src.modules.doctors.views.get_doctor_detail_service', return_value=({}, "SUCCESS"))
def test_public_doctor_detail_api(mock_svc, test_client):
    res = test_client.get('/api/v1/public/doctors/1')
    assert res.status_code == 200


@patch('src.modules.doctors.views.get_time_slots_service', return_value=([], "SUCCESS"))
def test_public_doctor_slots_api(mock_svc, test_client):
    res = test_client.get('/api/v1/public/doctors/1/time-slots?date=2026-04-12&serviceId=1')
    assert res.status_code == 200