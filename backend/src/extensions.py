from celery import Celery
from flask_caching import Cache
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
cache = Cache()
mail = Mail()
celery_app = Celery("medical_appointment_b3")
