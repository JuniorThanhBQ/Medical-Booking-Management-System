import logging
import time

from flask import g, jsonify, request
from werkzeug.exceptions import HTTPException
from werkzeug.middleware.proxy_fix import ProxyFix

logger = logging.getLogger('api_logger')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def setup_middlewares(app):
    if app.config.get("DEBUG") is False:
        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    @app.before_request
    def start_timer():
        g.start_time = time.time()

    @app.after_request
    def add_security_and_log(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'

        if hasattr(g, 'start_time'):
            elapsed_time = round((time.time() - g.start_time) * 1000, 2)
            logger.info(
                "[%s] %s - %d - %dms",
                request.method,
                request.path,
                response.status_code,
                elapsed_time
            )

        return response

    @app.errorhandler(Exception)
    def handle_exception(e):
        if isinstance(e, HTTPException):
            return jsonify({
                "status": "error",
                "code": e.code,
                "message": getattr(e, 'description', 'Unknown error')
            }), e.code

        logger.error("Server Error: %s", e)
        return jsonify({
            "status": "error",
            "code": 500,
            "message": "Internal Server Error."
        }), 500
