import requests
from config import Config

config = Config()

LOGIN_URL = "https://login.ah.nl/secure/oauth/authorize?client_id=appie&redirect_uri=appie://login-exit&response_type=code"
TOKEN_URL = "https://api.ah.nl/mobile-auth/v1/auth/token"
REFRESH_TOKEN_URL = "https://api.ah.nl/mobile-auth/v1/auth/token/refresh"
RECEIPTS_URL = "https://api.ah.nl/mobile-services/v1/receipts/"

def login():
    """Login to the API."""
    data = {
        "code": config.get("api")["code"],
        "clientId": "appie",
    }
    response = requests.post(TOKEN_URL, json=data, headers={"Content-Type": "application/json"})
    if response.status_code == 400 or response.status_code == 401:
        print("Please enter a new code. Refer to the README for more information.")
        print("https://login.ah.nl/secure/oauth/authorize?client_id=appie&redirect_uri=appie://login-exit&response_type=code")
        code = input("Code: ")
        data["code"] = code
        config.set("api", {"code": code, "refresh_token": "", "access_token": ""})
        response = requests.post(TOKEN_URL, json=data, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    tokens = response.json()
    data = {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "code": config.get("api")["code"],
    }
    config.set("api", data)
    return tokens


def update_tokens():
    """Update the access token and refresh token in the config file."""
    tokens = fetch_new_tokens()
    data = {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "code": config.get("api")["code"],
    }
    config.set("api", data)


def fetch_new_tokens():
    """Fetch new tokens using the refresh token."""
    data = {
        "refreshToken": config.get("api")["refresh_token"],
        "clientId": "appie",
    }
    response = requests.post(REFRESH_TOKEN_URL, json=data, headers={"Content-Type": "application/json"})
    if response.status_code == 400 or response.status_code == 401:
        return login()
    response.raise_for_status()
    return response.json()


def fetch_receipts():
    """Fetch the receipts from the API."""
    response = requests.get(RECEIPTS_URL, headers={"Authorization": f"Bearer {config.get('api')['access_token']}"})
    if response.status_code == 401:
        update_tokens()
        response = requests.get(RECEIPTS_URL, headers={"Authorization": f"Bearer {config.get('api')['access_token']}"})
    response.raise_for_status()
    return response.json()