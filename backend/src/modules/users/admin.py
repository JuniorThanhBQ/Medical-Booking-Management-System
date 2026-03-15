from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from src import db
from src.models import User


class UserAdmin(ModelView):
    column_list = ["id", "name", "email", "phone", "role", "gender", "created_date"]

    column_searchable_list = ["name", "email", "phone"]

    column_filters = ["role", "gender", "created_date"]

    column_sortable_list = ["id", "name", "created_date"]


def setup_admin(app):
    admin = Admin(app, name="Medical Admin", template_mode="bootstrap4")

    admin.add_view(UserAdmin(User, db.session))
