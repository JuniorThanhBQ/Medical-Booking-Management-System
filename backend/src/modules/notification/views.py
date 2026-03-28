from flask_restx import Namespace, Resource

from src.middlewares.auth import token_required
from src.modules.notification.services import (get_notifications_service,
                                               mark_notification_read_service)
from src.utils.utils import format_api_response

notification_namespace = Namespace("notifications", description="Thông báo hệ thống")


class NotificationAPI(Resource):
    method_decorators = [token_required]

    @notification_namespace.doc(security='api_key')
    def get(self, current_user):
        return format_api_response(*get_notifications_service(current_user))

    @notification_namespace.doc(security='api_key')
    def patch(self, current_user):
        return format_api_response(*mark_notification_read_service(current_user))
