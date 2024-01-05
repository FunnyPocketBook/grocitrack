from supermarktconnector.ah import AHConnector
from ah_api import search_all_products
import logging
import inflection
from database.DbHandler import DbHandler
from database.model import DbAHProducts
import datetime


def fetch_products() -> list[DbAHProducts]:
    connector = AHConnector()
    all_categories = connector.get_categories()
    all_products = []
    set_product_ids = set()
    date = datetime.datetime.now(datetime.timezone.utc)
    for category in all_categories:
        products_in_category = search_all_products(taxonomyId=category["id"])
        for product in products_in_category:
            if product["webshopId"] in set_product_ids:
                continue
            product = {
                inflection.underscore(key): value
                for key, value in product.items()
                if "virtual" not in key.lower()
                and key
                not in ["descriptionHighlights", "descriptionFull", "extraDescriptions"]
            }
            dbAHProduct = DbAHProducts(date_added=date, **product)
            all_products.append(dbAHProduct)
            set_product_ids.add(product["webshop_id"])
        log.info(f"Added products from category {category['name']}")
    return all_products


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
        level=logging.INFO,
        handlers=[logging.FileHandler("grocitrack.log"), logging.StreamHandler()],
    )
    log = logging.getLogger(__name__)
    db_handler = DbHandler()
    all_products = fetch_products()
    db_handler.add_ah_products(all_products)
