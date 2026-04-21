import os
from urllib.parse import quote


def check_env(env_name):
    env = os.getenv(env_name)
    if not env:
        raise ValueError(f"Thiếu biến môi trường bắt buộc: '{env_name}'")

    return env


class Config:
    PAGE_SIZE = 2
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY")
    CLOUDINARY_API_NAME = os.getenv("CLOUDINARY_API_NAME")
    CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
    CLOUDINARY_API_SECRETKEY = os.getenv("CLOUDINARY_API_SECRETKEY")

    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")
    CACHE_REDIS_HOST = os.getenv("CACHE_REDIS_HOST", "redis")
    CACHE_REDIS_PORT = os.getenv("CACHE_REDIS_PORT", "6379")
    CACHE_REDIS_DB = os.getenv("CACHE_REDIS_DB", "0")
    CACHE_DEFAULT_TIMEOUT = int(os.getenv("CACHE_DEFAULT_TIMEOUT", "500"))
    REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

    RABBITMQ_USERNAME = os.getenv("RABBITMQ_USERNAME", "guest")
    RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
    RABBITMQ_PORT = os.getenv("RABBITMQ_PORT", "5672")
    CELERY_BROKER_URL = f'amqp://{RABBITMQ_USERNAME}:{RABBITMQ_PASSWORD}@rabbitmq:{RABBITMQ_PORT}//'
    CELERY_RESULT_BACKEND = 'rpc://'

    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_SERVER = os.getenv("MAIL_SERVER", 'smtp.gmail.com')
    MAIL_USERNAME = os.getenv("MAIL_USERNAME", "2351050164thanh@ou.edu.vn")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.getenv("MAIL_DEFAULT_SENDER", "2351050164thanh@ou.edu.vn")

    APPLICATION_ROOT = '/'
    PREFERRED_URL_SCHEME = os.getenv('PREFERRED_URL_SCHEME', 'http')
    SERVER_NAME = os.getenv('SERVER_NAME', 'localhost:8000')

    EMAIL_VALIDATOR = os.getenv('EMAIL_VALIDATOR')
    FRONTEND_URL = os.getenv('FRONTEND_URL') or "https://resonate-proponent-thrower.ngrok-free.dev"
    WTF_CSRF_TRUSTED_ORIGINS = ['https://resonate-proponent-thrower.ngrok-free.dev']


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = "localhost"
    PORT = 8000
    DB_USER = os.getenv('DB_USER', 'root')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', "madb8")
    DB_PASSWORD = quote(os.getenv("DB_LOCAL_PASSWORD", ""))
    SQLALCHEMY_DATABASE_URI = (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@"
                               f"{DB_HOST}:3306/{DB_NAME}?charset=utf8mb4")
    ALLOWED_ORIGINS = ["*"]


class ProductionConfig(Config):
    DEBUG = False
    HOST = check_env("BACKEND_HOST")
    PORT = int(check_env("BACKEND_PORT"))
    DB_USER = check_env('DB_USER')
    DB_HOST = check_env('DB_HOST')
    DB_PASSWORD = quote(check_env("DB_PASSWORD"))
    DB_NAME = check_env('DB_NAME')
    SQLALCHEMY_DATABASE_URI = (f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
                               f"@{DB_HOST}:3306/{DB_NAME}?charset=utf8mb4")
    origins = os.getenv("ALLOWED_ORIGINS", "")

    if origins:
        ALLOWED_ORIGINS = origins.split(",")
    else:
        ALLOWED_ORIGINS = []
