import os

import cloudinary
from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_cors import CORS

from src.admin import init_admin
from src.extensions import db, limiter, login, migrate
from src.middlewares.middlewares import middlewares
from src.routes import api_v1

load_dotenv(find_dotenv())


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

    app.register_blueprint(api_v1)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    limiter.init_app(app)
    middlewares(app)
    init_admin(app, db)

    cloudinary.config(
        cloud_name=app.config.get("CLOUDINARY_API_NAME"),
        api_key=app.config.get("CLOUDINARY_API_KEY"),
        api_secret=app.config.get("CLOUDINARY_API_SECRETKEY"),
    )

    return app
