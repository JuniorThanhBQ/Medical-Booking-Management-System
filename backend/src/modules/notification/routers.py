from src.modules.notification.views import (NotificationDetailAPI,
                                            NotificationListAPI,
                                            notification_namespace)

notification_namespace.add_resource(NotificationListAPI, "")
notification_namespace.add_resource(NotificationDetailAPI, "/<int:notification_id>")
