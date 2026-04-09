from celery import Celery
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
cache = Cache()
limiter = Limiter(key_func=get_remote_address)
redis_client = FlaskRedis()
mail = Mail()
celery_app = Celery("medical_appointment_b3")
