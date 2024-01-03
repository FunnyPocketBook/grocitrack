import requests
import urllib.parse
from config import Config
import logging
import math

logging.getLogger("connectionpool").setLevel(logging.WARNING)

config = Config()

LOGIN_URL = "https://login.ah.nl/secure/oauth/authorize?client_id=appie&redirect_uri=appie://login-exit&response_type=code"
TOKEN_URL = "https://api.ah.nl/mobile-auth/v1/auth/token"
REFRESH_TOKEN_URL = "https://api.ah.nl/mobile-auth/v1/auth/token/refresh"
RECEIPTS_URL = "https://api.ah.nl/mobile-services/v1/receipts"
PREV_BOUGHT_URL = "https://api.ah.nl/mobile-services/product/search/v2/purchases?filters=previouslyBought%3Dpreviously_bought&sortOn=PURCHASE_DEPARTMENT&size=30&page=0"
HEADERS = {
    "Host": "api.ah.nl",
    "x-dynatrace": "MT_3_4_772337796_1_fae7f753-3422-4a18-83c1-b8e8d21caace_0_1589_109",
    "x-application": "AHWEBSHOP",
    "user-agent": "Appie/8.8.2 Model/phone Android/7.0-API24",
    "content-type": "application/json; charset=UTF-8",
}


def login():
    """Uses the code from the config file to fetch the access token and refresh token.

    Returns:
        dict: A dictionary containing the access token and refresh token."""
    data = {
        "code": config.get("api", "code"),
        "clientId": "appie",
    }
    response = requests.post(TOKEN_URL, json=data, headers=HEADERS)
    if response.status_code == 400 or response.status_code == 401:
        print("Please enter a new code. Refer to the README for more information.")
        print(LOGIN_URL)
        code = input("Code: ")
        data["code"] = code
        config.set("api", {"code": code, "refresh_token": "", "access_token": ""})
        response = requests.post(TOKEN_URL, json=data, headers=HEADERS)
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
    """Updates the access token and refresh token in the config file."""
    tokens = fetch_new_tokens()
    data = {
        "access_token": tokens["access_token"],
        "refresh_token": tokens["refresh_token"],
        "code": config.get("api", "code"),
    }
    config.set("api", data)


def fetch_new_tokens():
    """Fetches new tokens using the refresh token.

    Returns:
        dict: A dictionary containing the access token and refresh token."""
    data = {
        "refreshToken": config.get("api", "refresh_token"),
        "clientId": "appie",
    }
    response = requests.post(REFRESH_TOKEN_URL, json=data, headers=HEADERS)
    if response.status_code == 400 or response.status_code == 401:
        return login()
    response.raise_for_status()
    return response.json()


def fetch_receipts():
    """Fetches the receipts from the API.

    Returns:
        dict: A dictionary containing the receipts."""
    response = requests.get(
        RECEIPTS_URL,
        headers={
            **HEADERS,
            "Authorization": f"Bearer {config.get('api')['access_token']}",
        },
    )
    if response.status_code == 401:
        update_tokens()
        response = requests.get(
            RECEIPTS_URL,
            headers={
                **HEADERS,
                "Authorization": f"Bearer {config.get('api')['access_token']}",
            },
        )
    response.raise_for_status()
    return response.json()


def get_previously_bought(
    sort_on: str = "PURCHASE_DATE", size: int = 100, page: int = 0, result: list = None
):
    if result is None:
        result = []
    response = requests.get(
        "https://api.ah.nl/mobile-services/product/search/v2/purchases",
        headers={
            **HEADERS,
            "Authorization": f"Bearer {config.get('api')['access_token']}",
        },
        params={
            "filters": "previouslyBought%3Dpreviously_bought",
            "sortOn": sort_on,
            "size": size,
            "page": page,
        },
    )
    if response.status_code == 401:
        update_tokens()
        response = requests.get(
            PREV_BOUGHT_URL,
            headers={
                **HEADERS,
                "Authorization": f"Bearer {config.get('api')['access_token']}",
            },
        )
    response.raise_for_status()

    prev_bought = response.json()
    result.extend(prev_bought["products"])
    if "next" in prev_bought["links"]:
        url = prev_bought["links"]["next"]["href"]
        # get the page number and size from the url
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)
        page = int(params["page"][0])
        size = int(params["size"][0])
        get_previously_bought(page=page, size=size, result=result)
    return result


def search_products(query=None, page=0, size=750, sort="RELEVANCE", taxonomyId=None):
    size = math.floor(3000 / (page + 1))
    response = requests.get(
        "https://api.ah.nl/mobile-services/product/search/v2?sortOn=RELEVANCE",
        params={
            "sortOn": sort,
            "page": page,
            "size": size,
            "query": query,
            "taxonomyId": taxonomyId,
        },
        headers={
            **HEADERS,
            "Authorization": f"Bearer {config.get('api')['access_token']}",
        },
    )
    if response.status_code == 401:
        update_tokens()
        response = requests.get(
            "https://api.ah.nl/mobile-services/product/search/v2?sortOn=RELEVANCE",
            params={
                "sortOn": sort,
                "page": page,
                "size": size,
                "query": query,
                "taxonomyId": taxonomyId,
            },
            headers={
                **HEADERS,
                "Authorization": f"Bearer {config.get('api')['access_token']}",
            },
        )
    if not response.ok:
        response.raise_for_status()
    return response.json()


def search_all_products(**kwargs):
    """
    Iterate all the products available, filtering by query or other filters. Will return generator.
    :param kwargs: See params of 'search_products' method, note that size should not be altered to optimize/limit pages
    :return: generator yielding products
    """
    response = search_products(page=0, **kwargs)
    yield from response["products"]

    for page in range(1, response["page"]["totalPages"]):
        response = search_products(page=page, **kwargs)
        yield from response["products"]
