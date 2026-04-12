from datetime import date, datetime
from unittest.mock import MagicMock, patch

import pytest

from src.modules.appointments.models import StatusRole
from src.modules.appointments.services import (
    create_patient_appointment_service,
    create_receptionist_appointment_service, delete_appointment_service,
    get_appointment_detail_service, get_appointments_list_service,
    get_or_create_patient_profile, get_patient_profile_service,
    handle_date_update, handle_status_update, patch_appointment_service,
    validate_appointment_booking, validate_appointment_request,
    validate_doctor)


def test_get_appointments_list_service():
    mock_user = MagicMock()
    mock_user.profile.id = 1

    with patch('src.modules.appointments.services.get_appointments_base_query') as mock_query:
        mock_paginated = MagicMock()
        mock_paginated.items = []
        mock_query.return_value.filter.return_value.order_by.return_value.paginate.return_value = mock_paginated

        mock_user.role.name = "PATIENT"
        res, code = get_appointments_list_service(mock_user)
        assert code == "SUCCESS"

        mock_user.role.name = "DOCTOR"
        res, code = get_appointments_list_service(mock_user)
        assert code == "SUCCESS"

        mock_user.role.name = "RECEPTIONIST"
        mock_query.return_value.order_by.return_value.paginate.return_value = mock_paginated
        res, code = get_appointments_list_service(mock_user)
        assert code == "SUCCESS"

        mock_user.role.name = "UNKNOWN"
        res, code = get_appointments_list_service(mock_user)
        assert code == "FORBIDDEN"

@patch('src.modules.appointments.services.get_appointment_by_id')
@patch('src.modules.appointments.services.format_appointment', return_value={})
def test_get_appointment_detail_service(mock_format, mock_get):
    mock_user = MagicMock()
    mock_user.role.name = "PATIENT"
    mock_user.profile.id = 1

    mock_get.return_value = None
    res, code = get_appointment_detail_service(mock_user, 1)
    assert code == "NOT_FOUND"

    mock_apt = MagicMock()
    mock_apt.patient_profile_id = 2
    mock_get.return_value = mock_apt
    res, code = get_appointment_detail_service(mock_user, 1)
    assert code == "FORBIDDEN"

    mock_apt.patient_profile_id = 1
    res, code = get_appointment_detail_service(mock_user, 1)
    assert code == "SUCCESS"

@patch('src.modules.appointments.services.get_appointment_by_id')
def test_get_patient_profile_service(mock_get):
    mock_user = MagicMock()

    mock_user.role.name = "PATIENT"
    res, code = get_patient_profile_service(mock_user, 1)
    assert code == "FORBIDDEN"

    mock_user.role.name = "DOCTOR"
    mock_user.profile.id = 1

    mock_apt = MagicMock()
    mock_apt.doctor_profile_id = 1
    mock_get.return_value = mock_apt
    res, code = get_patient_profile_service(mock_user, 1)
    assert code == "SUCCESS"

@patch('src.modules.appointments.services.validate_appointment_booking')
@patch('src.modules.appointments.services.add_instance')
@patch('src.modules.appointments.services.commit_session')
@patch('src.modules.appointments.services.format_appointment', return_value={})
def test_create_patient_appointment_service(m_fmt, m_commit, m_add, m_val):
    mock_user = MagicMock()
    mock_user.role.name = "PATIENT"

    res, code = create_patient_appointment_service(mock_user, {})
    assert code == "ERROR_BAD_REQUEST"

    m_val.return_value = (datetime.now(), MagicMock(), MagicMock(), None)
    res, code = create_patient_appointment_service(mock_user, {
        "doctorId": 1, "appointmentDate": "2026-04-12T10:00:00Z", "medicalServiceId": 1
    })
    assert code == "SUCCESS"

@patch('src.modules.appointments.services.validate_appointment_booking')
@patch('src.modules.appointments.services.get_or_create_patient_profile')
@patch('src.modules.appointments.services.add_instance')
@patch('src.modules.appointments.services.commit_session')
@patch('src.modules.appointments.services.format_appointment', return_value={})
def test_create_receptionist_appointment_service(m_fmt, m_commit, m_add, m_prof, m_val):
    mock_user = MagicMock()
    mock_user.role.name = "RECEPTIONIST"

    res, code = create_receptionist_appointment_service(mock_user, {})
    assert code == "ERROR_BAD_REQUEST"

    m_val.return_value = (datetime.now(), MagicMock(), MagicMock(), None)
    m_prof.return_value = (MagicMock(), None)
    res, code = create_receptionist_appointment_service(mock_user, {"medicalServiceId": 1})
    assert code == "SUCCESS"