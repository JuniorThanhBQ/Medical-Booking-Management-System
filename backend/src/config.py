import os
from urllib.parse import quote


def check_env(env_name):
    env = os.getenv(env_name)
    if not env:
        raise ValueError(f"Thiếu env '{env_name}'")
    return env


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
    db_user = os.getenv('DB_USER', 'root')
    db_name = os.getenv('DB_NAME', 'madb8')
    db_password = quote(os.getenv("DB_PASSWORD", ''))
    default_url = \
        f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}?charset=utf8mb4"
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', default_url)
    ALLOWED_ORIGINS = ["*"]
    STORAGE_URI = os.getenv("RATELIMIT_STORAGE_URI", "memory://")


class ProductionConfig(Config):
    DEBUG = False
    HOST = os.getenv("PRODUCTION_HOST", "127.0.0.1")
    PORT = os.getenv("PORT", "8000")
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL_PROD')

    if not SQLALCHEMY_DATABASE_URI:
        production_user = check_env('DB_USER_PROD')
        production_db_host = check_env('DB_HOST_PROD')
        production_db_password = quote(check_env("DB_PASSWORD_PROD"))
        production_db = check_env('DB_NAME_PROD')
        SQLALCHEMY_DATABASE_URI = (f"mysql+pymysql://{production_user}:{production_db_password}"
                                   f"@{production_db_host}/{production_db}?charset=utf8mb4")

    origins = os.getenv("ALLOWED_ORIGINS", "")

    if origins:
        ALLOWED_ORIGINS = origins.split(",")
    else:
        ALLOWED_ORIGINS = []

    CACHE_TYPE = "RedisCache"
    CACHE_DEFAULT_TIMEOUT = 300
    CACHE_REDIS_URL = check_env("REDIS_URL")
    STORAGE_URI = check_env("RATELIMIT_STORAGE_URI")
