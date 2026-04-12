import os

import cloudinary
from celery.schedules import crontab
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_cors import CORS

import src.modules.notification.rabbitmq  # noqa: F401
from src.admin import init_admin
from src.extensions import cache, celery_app, db, login, mail, migrate
from src.middlewares.middlewares import middlewares
from src.routes import api_v1

load_dotenv(find_dotenv())

def init_celery(app, celery):
    celery.conf.update(
        broker_url=app.config.get('CELERY_BROKER_URL'),
        result_backend=app.config.get('CELERY_RESULT_BACKEND'),
        include=['src.modules.notification.rabbitmq.tasks'],
        enable_utc=False,
        timezone="Asia/Ho_Chi_Minh"
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask

    celery.conf.beat_schedule = {
        'daily-reminder-at-15pm': {
            'task': 'src.modules.notification.rabbitmq.tasks.reminders_task_schedule',
            'schedule': crontab(minute=0, hour=15),
        },
        'check-pending-emails-8-hours': {
            'task': 'src.modules.notification.rabbitmq.tasks.pending_emails_task_schedule',
            'schedule': crontab(minute=0, hour='*/8'),
        },
    }


def create_app():
    app = Flask(__name__)
    flask_mode = os.getenv("FLASK_MODE")

    if flask_mode == "production":
        app.config.from_object("src.config.ProductionConfig")
    else:
        app.config.from_object("src.config.DevelopmentConfig")

    CORS(app, resources={
        r"/*": {
            "origins": app.config.get("ALLOWED_ORIGINS", "*"),
            "methods": ["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Authorization"],
            "supports_credentials": True
        }
    })

    middlewares(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    init_admin(app, db)
    cache.init_app(app)
    mail.init_app(app)
    init_celery(app, celery_app)

    app.register_blueprint(api_v1)

    cloudinary.config(
        cloud_name=app.config.get("CLOUDINARY_API_NAME"),
        api_key=app.config.get("CLOUDINARY_API_KEY"),
        api_secret=app.config.get("CLOUDINARY_API_SECRETKEY"),
    )

    return app
