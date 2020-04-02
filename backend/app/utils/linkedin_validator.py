import requests

from settings import LINKEDIN_URL


def validate_token(token: str):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return requests.get(LINKEDIN_URL, headers=headers)
