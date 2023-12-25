from ah_api import fetch_receipts, get_previously_bought
from config import Config
from supermarktconnector.ah import AHConnector
import logging

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(module)s: %(message)s", level=logging.WARN,
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])
log = logging.getLogger(__name__)
config = Config()
timeout = 3

connector = AHConnector()

def fetch_products():
    list_all_products = []
    all_products = connector.search_all_products()
    for products in all_products:
        list_all_products.append(products)
    print(len(list_all_products))
    return list_all_products

fetch_products()