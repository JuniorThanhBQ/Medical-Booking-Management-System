from src.modules.notification.views import (NotificationAPI,
                                            notification_namespace)

notification_namespace.add_resource(NotificationAPI, "", "/<int:notification_id>")
