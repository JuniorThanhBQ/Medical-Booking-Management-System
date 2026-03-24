from flask_restful import Resource

from src.modules.auth_profile.auth_decorators import token_required
from src.modules.notification.services import (get_notifications_service,
                                               mark_notification_read_service)
from src.utils.utils import format_api_response


class NotificationAPI(Resource):
    method_decorators = [token_required]

    def get(self, current_user):
        return format_api_response(*get_notifications_service(current_user))

    def patch(self, current_user):
        return format_api_response(*mark_notification_read_service(current_user))
