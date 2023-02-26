import requests
from config import Config

config = Config()

LOGIN_URL = "https://loyalty-app.jumbo.com/user/login"
TOKEN_URL = "https://api.ah.nl/mobile-auth/v1/auth/token"
REFRESH_TOKEN_URL = "https://loyalty-app.jumbo.com/api/auth/refresh"
RECEIPTS_URL = "https://loyalty-app.jumbo.com/api/receipt/customer/overviews"

def login():
    """Uses the code from the config file to fetch the access token and refresh token.
    
    Returns:
        dict: A dictionary containing the access token and refresh token."""
    data = {
        "code": config.get("api", "code"),
        "clientId": "appie",
    }
    response = requests.post(TOKEN_URL, json=data, headers={"Content-Type": "application/json"})
    if response.status_code == 400 or response.status_code == 401:
        print("Please enter a new code. Refer to the README for more information.")
        print(LOGIN_URL)
        code = input("Code: ")
        data["code"] = code
        config.set("api", {"code": code, "refresh_token": "", "access_token": ""})
        response = requests.post(TOKEN_URL, json=data, headers={"Content-Type": "application/json"})
    response.raise_for_status()
    tokens = response.json()
    data = {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "code": config.get("api", "code"),
    }
    config.set("api", data)
    return tokens


def update_tokens():
    """Fetches new tokens using the refresh token.
    
    Returns:
        dict: A dictionary containing the access token and refresh token."""
    data = {
        "refreshToken": config.get('jumbo', 'refresh_token'),
    }
    response = requests.post(REFRESH_TOKEN_URL, json=data, headers={"Content-Type": "application/json"})
    if response.status_code == 400 or response.status_code == 401:
        return login()
    response.raise_for_status()
    tokens = response.json()
    data = {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
    }
    config.set("jumbo", data)
    return data


def fetch_receipts():
    """Fetches the receipts from the API.
    
    Returns:
        dict: A dictionary containing the receipts."""
    response = requests.get(RECEIPTS_URL, headers={"Authorization": f"Bearer {config.get('jumbo')['access_token']}"})
    if response.status_code == 401:
        update_tokens()
        response = requests.get(RECEIPTS_URL, headers={"Authorization": f"Bearer {config.get('jumbo')['access_token']}"})
    response.raise_for_status()
    return response.json()