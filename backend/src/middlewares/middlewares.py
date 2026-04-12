import logging
import time

from flask import g, request
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

logger = logging.getLogger('flask_logger')

if not logger.handlers:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def middlewares(app):
    if app.config.get("DEBUG") is False:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    @app.before_request
    def start_timer():
        g.start_time = time.time()


    @app.after_request
    def add_security_headers(response):
        response.headers['Content-Security-Policy'] = (
            "default-src 'self'; "
            "img-src 'self' data: https://res.cloudinary.com; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
        )

        return response

    @app.after_request
    def log_request(response):
        if hasattr(g, 'start_time'):
            finished_time = round((time.time() - g.start_time) * 1000, 2)
            logger.info(
                "[%s] %s - %d - %dms",
                request.method,
                request.path,
                response.status_code,
                finished_time
            )
        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return {
                "status": "error",
                "code": e.code,
                "message": getattr(e, 'description', 'Lỗi không xác định')
            }, e.code

        logger.error("Server Error: %s", str(e), exc_info=True)

        return {
            "status": "error",
            "code": 500,
            "message": "Internal Server Error."
        }, 500
