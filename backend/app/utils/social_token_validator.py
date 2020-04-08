import requests

from settings import LINKEDIN_URL, GOOGLE_URL, FACEBOOK_URL


def validate_linkedin(token: str):
    headers = _get_auth_header(token)
    return requests.get(LINKEDIN_URL, headers=headers)


def validate_google(token: str):
    headers = _get_auth_header(token)
    return requests.get(GOOGLE_URL, headers=headers)

def validate_facebook(token: str):
    headers = _get_auth_header(token)
    return requests.get(FACEBOOK_URL, headers=headers)


def _get_auth_header(token: str):
    return {
        "Authorization": f"Bearer {token}"
    }
