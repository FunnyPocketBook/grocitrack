from database.DbHandler import DbHandler
from ah_api import fetch_receipts
from config import Config
from classes.Receipt import Receipt
from supermarktconnector.ah import AHConnector
from classes.Category import Category
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import pickle
import random
import time
import logging

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(module)s: %(message)s", level=logging.INFO,
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])
log = logging.getLogger(__name__)
config = Config()

def get_category(category: dict, parent: Category=None):
    r = random.randint(1, 100)
    if r > 90:
        print(f"Sleeping for 10 seconds to avoid rate limit")
        time.sleep(10)
    connector = AHConnector()
    category = Category(category["id"], category["name"], category["slugifiedName"], images=category["images"])
    if parent:
        parent.add_child(category)
        category.set_parent(parent)
    try:
        children = connector.get_sub_categories(category.taxonomy_id)["children"]
        print(f"Getting children of {category.name}")
        if children:
            get_categories(children, category)
    except Exception as e:
        print(f"Error getting subcategories of {category.name}: {e}")
    return category


def get_categories(categories: list, parent: Category=None, result: list=[]):
    result = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(get_category, category, parent) for category in categories]
        for future in as_completed(futures):
            result.append(future.result())
    return result


def add_categories(db_handler: DbHandler):
    if os.path.exists("src/database/categories.sql"):
        log.info("Creating categories table from SQL file")
        db_handler.execute_sql_file("src/database/categories.sql")
        db_handler.execute_sql_file("src/database/categories_hierarchy.sql")
    else:
        if os.path.exists("categories.pickle"):
            with open("categories.pickle", "rb") as f:
                categories = pickle.load(f)
        else:
            connector = AHConnector()
            categories = connector.get_categories()
            result = []
            categories = get_categories(categories, result=result)
            print(result)
        for category in categories:
            db_handler.add_category(category)


def main():
    db_handler = DbHandler()
    if not db_handler.get_categories():
        add_categories(db_handler)

    receipts_result = fetch_receipts()

    receipts = [Receipt(receipt) for receipt in receipts_result if db_handler.find_receipt(receipt["transactionId"]) is None]

    for receipt in receipts:
        if receipt.is_empty():
            continue
        receipt.set_details()
        location = receipt.location
        dbLocation = db_handler.find_location(location.name)
        if not dbLocation:
            dbLocation = db_handler.add_location(location)
        dbReceipt = db_handler.add_receipt(receipt, dbLocation.id)   
        db_handler.add_products(receipt.products, dbReceipt.id)
        db_handler.add_discounts(receipt.discounts["discounts"], dbReceipt.id)
        db_handler.set_categories_for_products(receipt.products)

    db_handler.close()
    log.info(f"Added {len(receipts)} new receipts to the database.")

if __name__ == "__main__":
    main()