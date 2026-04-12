from datetime import date, datetime
from unittest.mock import MagicMock, patch

import pytest

from src.modules.appointments.models import StatusRole
from src.modules.medical_records.models import MedicalRecordType
from src.modules.medical_records.services import (
    _check_record_access_permission, create_medical_record_service,
    get_detail_medical_record_service, get_list_medical_record_service,
    update_medical_record_service)


@patch('src.modules.medical_records.services.get_appointment_by_id')
@patch('src.modules.medical_records.services.add_instance')
@patch('src.modules.medical_records.services.flush_session')
@patch('src.modules.medical_records.services.commit_session')
def test_create_medical_record_service(m_commit, m_flush, m_add, m_get):
    mock_user = MagicMock()
    mock_user.role.name = "PATIENT"

    res, code = create_medical_record_service(mock_user, 1, {})
    assert code == "FORBIDDEN"

    mock_user.role.name = "DOCTOR"
    mock_user.profile.id = 1

    m_get.return_value = None
    res, code = create_medical_record_service(mock_user, 1, {})
    assert code == "NOT_FOUND"

    mock_apt = MagicMock()
    mock_apt.doctor_profile_id = 2
    m_get.return_value = mock_apt
    res, code = create_medical_record_service(mock_user, 1, {})
    assert code == "FORBIDDEN"

    mock_apt.doctor_profile_id = 1
    mock_apt.medical_record = True
    res, code = create_medical_record_service(mock_user, 1, {})
    assert code == "BAD_REQUEST"

    mock_apt.medical_record = None
    res, code = create_medical_record_service(mock_user, 1, {"status": "DONE"})
    assert code == "SUCCESS"
    assert "diagnosis" in res

@patch('src.modules.medical_records.services.get_medical_record_by_id')
@patch('src.modules.medical_records.services.commit_session')
def test_update_medical_record_service(m_commit, m_get):
    mock_user = MagicMock()
    mock_user.role.name = "DOCTOR"
    mock_user.profile.id = 1

    mock_rec = MagicMock()
    mock_rec.doctor_profile_id = 1
    m_get.return_value = mock_rec

    res, code = update_medical_record_service(mock_user, 1, {"status": "FOLLOW_UP", "diagnosis": "Sốt"})
    assert code == "SUCCESS"
    assert mock_rec.diagnosis == "Sốt"

@patch('src.modules.medical_records.services.get_medical_record_by_id')
def test_get_detail_medical_record_service(m_get):
    mock_user = MagicMock()
    mock_user.role.name = "PATIENT"
    mock_user.profile.id = 1

    mock_rec = MagicMock()
    mock_rec.patient_profile_id = 1
    m_get.return_value = mock_rec

    res, code = get_detail_medical_record_service(mock_user, 1)
    assert code == "SUCCESS"

    mock_rec.patient_profile_id = 2
    res, code = get_detail_medical_record_service(mock_user, 1)
    assert code == "FORBIDDEN"

@patch('src.modules.medical_records.services.get_medical_records_by_role')
def test_get_list_medical_record_service(m_get_role):
    mock_user = MagicMock()

    mock_user.role.name = "RECEPTIONIST"
    res, code = get_list_medical_record_service(mock_user, {})
    assert code == "FORBIDDEN"

    mock_user.role.name = "PATIENT"
    mock_user.profile = None
    res, code = get_list_medical_record_service(mock_user, {})
    assert code == "FORBIDDEN"

    mock_user.profile = MagicMock()
    mock_user.profile.id = 1

    mock_paginated = MagicMock()
    mock_paginated.items = []
    m_get_role.return_value = mock_paginated

    res, code = get_list_medical_record_service(mock_user, {"page": 1, "limit": 10})
    assert code == "SUCCESS"