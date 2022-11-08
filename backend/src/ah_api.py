import requests
import yaml
from classes import Receipt

config = {}

TOKEN_URL = "https://api.ah.nl/mobile-auth/v1/auth/token"
REFRESH_TOKEN_URL = "https://api.ah.nl/mobile-auth/v1/auth/token/refresh"
RECEIPTS_URL = "https://api.ah.nl/mobile-services/v1/receipts/"

def login():
    """Login to the API."""
    data = {
        "code": config["api"]["code"],
        "clientId": "appie",
    }
    response = requests.post(TOKEN_URL, json=data, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    tokens = response.json()
    config["api"]["access_token"] = tokens["access_token"]
    config["api"]["refresh_token"] = tokens["refresh_token"]
    with open("config.yml", "w") as f:
        yaml.dump(config, f)
    return tokens


def update_tokens():
    """Update the access token and refresh token in the config file."""
    tokens = fetch_new_tokens()
    config["api"]["access_token"] = tokens["access_token"]
    config["api"]["refresh_token"] = tokens["refresh_token"]
    with open("config.yml", "w") as f:
        yaml.dump(config, f)

def fetch_new_tokens():
    """Fetch new tokens using the refresh token."""
    data = {
        "refreshToken": config["api"]["refresh_token"],
        "clientId": "appie",
    }
    response = requests.post(REFRESH_TOKEN_URL, json=data, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    return response.json()


def fetch_receipts():
    """Fetch the receipts from the API."""
    response = requests.get(RECEIPTS_URL, headers={"Authorization": f"Bearer {config['api']['access_token']}"})
    if response.status_code == 401:
        update_tokens()
        response = requests.get(RECEIPTS_URL, headers={"Authorization": f"Bearer {config['api']['access_token']}"})
    response.raise_for_status()
    result = response.json()

    receipts = [Receipt(receipt) for receipt in result]
    return receipts