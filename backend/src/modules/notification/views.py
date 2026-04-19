from dependency_injector.wiring import Provide, inject
from flask_restx import Resource

from src.containers import AppContainer
from src.middlewares.auth import auth_required
from src.modules.notification import notification_namespace
from src.utils.utils import format_api_response

pagination_parser = notification_namespace.parser()
pagination_parser.add_argument('page', type=int, required=False, default=1, help='Số trang hiện tại')
pagination_parser.add_argument('per_page', type=int, required=False, default=10, help='Số thông báo trên 1 trang')


class NotificationListAPI(Resource):
    method_decorators = [auth_required]

    @notification_namespace.doc(security='api_key', parser=pagination_parser)
    @inject
    def get(self, current_user, notification_services=
    Provide[AppContainer.notification_app.notification_services]):
        args = pagination_parser.parse_args()
        return format_api_response(*notification_services.get_notifications_service(
            current_user, args['page'], args['per_page']))

    @notification_namespace.doc(security='api_key')
    @inject
    def patch(self, current_user, notification_services=
    Provide[AppContainer.notification_app.notification_services]):
        return format_api_response(*notification_services.mark_all_notification_service(current_user))


class NotificationDetailAPI(Resource):
    method_decorators = [auth_required]

    @notification_namespace.doc(security='api_key')
    @inject
    def get(self, current_user, notification_id, notification_services=
    Provide[AppContainer.notification_app.notification_services]):
        return format_api_response(*notification_services.get_detail_notification_service(
            current_user, notification_id))

    @notification_namespace.doc(security='api_key')
    @inject
    def patch(self, current_user, notification_id, notification_services=
    Provide[AppContainer.notification_app.notification_services]):
        return format_api_response(*notification_services.mark_detail_notification_service(
            current_user, notification_id))

    @notification_namespace.doc(security='api_key')
    @inject
    def delete(self, current_user, notification_id, notification_services=
    Provide[AppContainer.notification_app.notification_services]):
        return format_api_response(*notification_services.delete_notification_service(
            current_user, notification_id))
