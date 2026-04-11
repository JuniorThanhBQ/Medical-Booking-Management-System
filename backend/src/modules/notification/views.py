from flask_restx import Resource

from src.middlewares.auth import auth_required
from src.modules.notification import notification_namespace
from src.modules.notification.services import (
    delete_notification_service, get_detail_notification_service,
    get_notifications_service, mark_all_notification_service,
    mark_detail_notification_service)
from src.utils.utils import format_api_response

pagination_parser = notification_namespace.parser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Số trang hiện tại')
pagination_parser.add_argument('per_page', type=int, required=False, default=10, help='Số thông báo trên 1 trang')


class NotificationListAPI(Resource):
    method_decorators = [auth_required]

    @notification_namespace.doc(security='api_key', parser=pagination_parser)
    def get(self, current_user):
        args = pagination_parser.parse_args()
        return format_api_response(*get_notifications_service(current_user, args['page'], args['per_page']))

    @notification_namespace.doc(security='api_key')
    def patch(self, current_user):
        return format_api_response(*mark_all_notification_service(current_user))


class NotificationDetailAPI(Resource):
    method_decorators = [auth_required]

    @notification_namespace.doc(security='api_key')
    def get(self, current_user, notification_id):
        return format_api_response(*get_detail_notification_service(current_user, notification_id))

    @notification_namespace.doc(security='api_key')
    def patch(self, current_user, notification_id):
        return format_api_response(*mark_detail_notification_service(current_user, notification_id))

    @notification_namespace.doc(security='api_key')
    def delete(self, current_user, notification_id):
        return format_api_response(*delete_notification_service(current_user, notification_id))
