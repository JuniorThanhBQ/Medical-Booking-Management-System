from unittest.mock import MagicMock, patch

from src.libs.email_validator import verify_email_existence
from tests.test_base import test_app


def test_verify_email_existence_missing_params():
    assert verify_email_existence(None, None) is False


def test_verify_email_existence_deliverable(test_app):
    fake_resp = MagicMock()
    fake_resp.raise_for_status.return_value = None
    fake_resp.json.return_value = {
        'email_deliverability': {'status': 'DELIVERABLE'}
    }

    with patch('src.libs.email_validator.requests.get', return_value=fake_resp):
        assert verify_email_existence('key', 'a@b.com') is True


def test_verify_email_existence_api_error(test_app):
    with patch('src.libs.email_validator.requests.get', side_effect=Exception('fail')):
        assert verify_email_existence('key', 'a@b.com') is False
