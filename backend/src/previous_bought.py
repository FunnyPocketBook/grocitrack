import inflection
import logging

from ah_api import get_previously_bought
from database.DbHandler import DbHandler
from database.model import DbPreviousProducts

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)
log = logging.getLogger(__name__)


def fetch_previous_bought():
    prev_bought = get_previously_bought()

    set_product_ids = set()
    previous_products = []
    for product in prev_bought:
        product["webshopId"] = str(product["webshopId"])
        if product["webshopId"] in set_product_ids:
            continue
        product = {
            inflection.underscore(key): value
            for key, value in product.items()
            if "virtual" not in key.lower()
        }
        dbPrevProduct = DbPreviousProducts(**product)
        previous_products.append(dbPrevProduct)
        set_product_ids.add(product["webshop_id"])
    return previous_products


if __name__ == "__main__":
    db_handler = DbHandler()
    previous_products = fetch_previous_bought()
    db_handler.add_prev_products(previous_products)
