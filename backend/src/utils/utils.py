import logging
import os

from google.auth.transport import requests
from google.oauth2 import id_token


def verify_google_token(token):
    try:
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID")
        )
        return id_info

    except Exception as ex:
        logging.error(f"Lỗi trong xác thực google token: {ex}")
        return None
