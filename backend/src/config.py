import os
from urllib.parse import quote


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PAGE_SIZE = 2
    CLOUDINARY_API_NAME = os.getenv("CLOUDINARY_API_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRETKEY = os.getenv("CLOUDINARY_API_SECRETKEY")


class DevelopmentConfig(Config):
    RUN_MODE = True
    HOST = os.getenv("DEVELOPMENT_HOST", "127.0.0.1")
    PORT = 8000
    db_password = quote(str(os.getenv("DB_PASSWORD", "")))
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{db_password}@localhost/{os.getenv('DB_NAME')}?charset=utf8mb4"


class ProductionConfig(Config):
    RUN_MODE = False
    HOST = os.getenv("PRODUCTION_HOST")
    PORT = int(os.getenv("PORT", 8000))
    production_db_password = quote(str(os.getenv("PRODUCTION_DB_PASSWORD", "")))
    production_db_user = os.getenv("PRODUCTION_DB_USER", "")
    production_db_host = os.getenv("PRODUCTION_DB_HOST", "localhost")
    production_db_name = os.getenv("PRODUCTION_DB_NAME", "")
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{production_db_user}:{production_db_password}@{production_db_host}/{production_db_name}?charset=utf8mb4"
