from unittest.mock import MagicMock, patch
from tests.test_base import test_app
import src


def test_celery():
    mock_app = MagicMock()
    mock_app.config = {
        'CELERY_BROKER_URL': 'redis://localhost',
        'CELERY_RESULT_BACKEND': 'redis://localhost'
    }
    mock_celery = MagicMock()

    src.init_celery(mock_app, mock_celery)

    assert mock_celery.conf.update.called
    assert 'daily-reminder-at-15pm' in mock_celery.conf.beat_schedule
