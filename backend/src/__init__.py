import os
from pathlib import Path

import cloudinary
from dotenv import load_dotenv
from flask import Flask

from src.extensions import db, limiter, login, migrate
from src.modules.auth_profile import models
from src.routes import api_v1

env_path = Path(__file__).resolve().parent.parent / ".env"

if env_path.exists():
    load_dotenv(env_path)
else:
    raise SystemError("Lỗi hệ thống thiếu file env")


def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_v1)
    flask_mode = os.getenv("FLASK_MODE")

    if flask_mode == "production":
        app.config.from_object("src.config.ProductionConfig")
    else:
        app.config.from_object("src.config.DevelopmentConfig")

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    limiter.init_app(app)

    cloudinary.config(
        cloud_name=app.config["CLOUDINARY_API_NAME"],
        api_key=app.config["CLOUDINARY_API_KEY"],
        api_secret=app.config["CLOUDINARY_API_SECRETKEY"],
    )

    return app
