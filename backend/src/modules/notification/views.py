from flask_restful import Resource

from src.utils.utils import format_api_response

from src.utils.decorator import token_required
from .services import get_notifications_service, mark_notification_read_service


class NotificationAPI(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        return format_api_response(*get_notifications_service(current_user))

    def patch(self, current_user):
        return format_api_response(*mark_notification_read_service(current_user))
