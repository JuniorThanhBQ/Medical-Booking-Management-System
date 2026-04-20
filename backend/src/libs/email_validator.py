import requests
from flask import current_app


def verify_email_existence(api_key=None, email=None):
    if not api_key or not email:
        return False

    url = "https://emailreputation.abstractapi.com/v2/"

    params = {
        "api_key": api_key,
        "email": email
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        deliverability_data = data.get('email_deliverability', {})
        status = deliverability_data.get('status', '').lower()
        return status == 'deliverable'

    except Exception as e:
        current_app.logger.error(f"Xác thực email thất bại: {str(e)}")
        return False
