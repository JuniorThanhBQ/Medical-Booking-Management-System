from flask import Blueprint
from flask_restful import Api

from src.modules.notification.views import NotificationAPI

notification_blueprint = Blueprint("notification", __name__)
api = Api(notification_blueprint)

api.add_resource(NotificationAPI, "", "/<int:notification_id>")
