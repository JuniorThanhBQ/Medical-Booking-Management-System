import os

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
limiter = Limiter(key_func=get_remote_address,
                  storage_uri=os.environ.get("RATELIMIT_STORAGE_URI", "memory://"))
