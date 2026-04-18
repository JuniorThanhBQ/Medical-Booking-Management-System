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
            username="notif_user", password=generate_password_hash("Pass@123"),
            email="notif@test.com", first_name="Notif", last_name="User", role=UserRole.PATIENT
        )
        add_user(user)
        commit()
        token = create_token(user)

    test_client.environ_base['HTTP_AUTHORIZATION'] = f"Bearer {token}"
    return test_client


@patch('src.modules.notification.views.get_notifications_service', return_value=({"items": []}, "SUCCESS"))
@patch('src.modules.notification.views.mark_all_notification_service', return_value=({}, "SUCCESS"))
def test_notification_list_api(mock_mark, mock_get, auth_client):
    res = auth_client.get('/api/v1/notifications?page=1&per_page=10')
    assert res.status_code == 200

    res = auth_client.patch('/api/v1/notifications')
    assert res.status_code == 200


@patch('src.modules.notification.views.get_detail_notification_service', return_value=({"id": 1}, "SUCCESS"))
@patch('src.modules.notification.views.mark_detail_notification_service', return_value=({}, "SUCCESS"))
@patch('src.modules.notification.views.delete_notification_service', return_value=({}, "SUCCESS"))
def test_notification_detail_api(mock_delete, mock_mark, mock_get, auth_client):
    res = auth_client.get('/api/v1/notifications/1')
    assert res.status_code == 200

    res = auth_client.patch('/api/v1/notifications/1')
    assert res.status_code == 200

    res = auth_client.delete('/api/v1/notifications/1')
    assert res.status_code == 200