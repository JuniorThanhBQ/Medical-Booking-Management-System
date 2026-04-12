from unittest.mock import MagicMock, patch

import pytest

from src.modules.notification.services import (
    delete_notification_service, get_detail_notification_service,
    get_notifications_service, insert_appointment_notifications,
    mark_all_notification_service, mark_detail_notification_service)


@patch('src.modules.notification.services.get_paginated_by_user_id')
def test_get_notifications_service(mock_get_paginated):
    mock_paginated = MagicMock()
    mock_item = MagicMock(id=1, title="Test", message="Msg", is_read=False)
    mock_item.type.name = "SYSTEM"
    mock_item.created_date.isoformat.return_value = "2026-04-12T10:00:00"

    mock_paginated.items = [mock_item]
    mock_get_paginated.return_value = mock_paginated

    res, code = get_notifications_service(MagicMock(id=1))
    assert code == "SUCCESS"
    assert len(res["items"]) == 1


@patch('src.modules.notification.services.get_by_id_and_user_id')
def test_get_detail_notification_service(mock_get_by_id):
    mock_get_by_id.return_value = None
    res, code = get_detail_notification_service(MagicMock(id=1), 1)
    assert code == "NOT_FOUND"

    mock_item = MagicMock(id=1)
    mock_item.type.name = "SYSTEM"
    mock_get_by_id.return_value = mock_item
    res, code = get_detail_notification_service(MagicMock(id=1), 1)
    assert code == "SUCCESS"


@patch('src.modules.notification.services.get_unread_by_user_id')
@patch('src.modules.notification.services.bulk_mark_as_read')
def test_mark_all(mock_bulk, mock_get_unread):
    mock_get_unread.return_value = [MagicMock()]
    res, code = mark_all_notification_service(MagicMock(id=1))
    assert code == "SUCCESS"
    assert mock_bulk.called


@patch('src.modules.notification.services.get_by_id_and_user_id')
@patch('src.modules.notification.services.commit')
def test_mark_detail(mock_commit, mock_get_by_id):
    mock_get_by_id.return_value = None
    res, code = mark_detail_notification_service(MagicMock(id=1), 1)
    assert code == "NOT_FOUND"

    mock_item = MagicMock(is_read=False)
    mock_get_by_id.return_value = mock_item
    res, code = mark_detail_notification_service(MagicMock(id=1), 1)
    assert code == "SUCCESS"
    assert mock_item.is_read is True


@patch('src.modules.notification.services.get_by_id_and_user_id')
@patch('src.modules.notification.services.delete_notification')
def test_delete_service(mock_del, mock_get_by_id):
    mock_get_by_id.return_value = None
    res, code = delete_notification_service(MagicMock(id=1), 1)
    assert code == "NOT_FOUND"

    mock_get_by_id.return_value = MagicMock()
    res, code = delete_notification_service(MagicMock(id=1), 1)
    assert code == "SUCCESS"


@patch('src.modules.notification.services.get_doctor_user_info')
@patch('src.modules.notification.services.get_patient_user_info')
@patch('src.modules.notification.services.insert_notifications_list')
def test_insert_appointment_notifications(mock_insert, mock_patient, mock_doc):
    mock_apt = MagicMock(doctor_profile_id=1, patient_profile_id=2, name="Kham")

    mock_doc.return_value = None
    assert insert_appointment_notifications(mock_apt, MagicMock(), "Action") is None

    mock_doc.return_value = MagicMock(last_name="A", first_name="B")
    mock_patient.return_value = MagicMock(last_name="C", first_name="D")
    mock_insert.return_value = [1, 2]

    res = insert_appointment_notifications(mock_apt, MagicMock(), "Action")
    assert res == [1, 2]

    mock_insert.side_effect = Exception("DB Error")
    with patch('src.modules.notification.services.rollback'):
        with pytest.raises(Exception):
            insert_appointment_notifications(mock_apt, MagicMock(), "Action")