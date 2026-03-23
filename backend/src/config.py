import os
from urllib.parse import quote


class Config:
    PAGE_SIZE = 2
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CLOUDINARY_API_NAME = os.getenv("CLOUDINARY_API_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRETKEY = os.getenv("CLOUDINARY_API_SECRETKEY")


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = 8000
    db_host = os.getenv('DB_HOST', 'localhost')
    db_password = quote(str(os.getenv("DB_PASSWORD")))
    default_db_url = f"mysql+pymysql://{os.getenv('DB_USER')}:{db_password}@{db_host}/{os.getenv('DB_NAME')}?charset=utf8mb4"  # pylint: disable=line-too-long
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default_db_url)
    ALLOWED_ORIGINS = ["*"]


class ProductionConfig(Config):
    DEBUG = False
    HOST = os.getenv("PRODUCTION_HOST")
    PORT = os.getenv("PORT")
    db_host = os.getenv('DB_HOST', 'localhost')
    production_db_password = quote(str(os.getenv("PRODUCTION_DB_PASSWORD")))
    default_db_url = f"mysql+pymysql://{os.getenv('PRODUCTION_DB_USER')}:{production_db_password}@{os.getenv('PRODUCTION_DB_HOST')}/{os.getenv('PRODUCTION_DB_NAME')}?charset=utf8mb4"  # pylint: disable=line-too-long
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default_db_url)
    origins = os.getenv("ALLOWED_ORIGINS", "")
    ALLOWED_ORIGINS = origins.split(",") if origins else []
