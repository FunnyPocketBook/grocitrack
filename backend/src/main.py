from database.DbHandler import DbHandler
from ah_api import fetch_receipts
from config import Config
from classes.Receipt import Receipt
from supermarktconnector.ah import AHConnector
from classes.Category import Category
from concurrent.futures import ThreadPoolExecutor, as_completed
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
    # get random number
    r = random.randint(1, 100)
    # if the number is 1, sleep for 1 second
    if r > 90:
        print(f"Sleeping for 10 seconds because r is {r}")
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


# tail recursive function to get all the categories. Make it concurrent
def get_categories(categories: list, parent: Category=None, result: list=[]):
    result = []
    with ThreadPoolExecutor(max_workers=2) as executor:
        futures = [executor.submit(get_category, category, parent) for category in categories]
        for future in as_completed(futures):
            result.append(future.result())
    return result

    # for category in categories:
    #     category = Category(category["id"], category["name"], category["slugifiedName"], images=category["images"])
    #     if parent:
    #         parent.add_child(category)
    #         category.set_parent(parent)
    #     children = connector.get_sub_categories(category.taxonomy_id)["children"]
    #     print(f"Getting children of {category.name}")
    #     if children:
    #         get_categories(children, category, connector)
    #     result.append(category)
    # return result


def main():
    db_handler = DbHandler()

    # get all categories from the database. If there are none, add them.
    
    # TODO: Get the categories of the product. This is a bit tricky because the API doesn't return all the categories of the product. It only returns the immediate category of the product. So we need to do the following and then match the product category to the category in the list:
    # 1. Get all the categories that exist with https://api.ah.nl/mobile-services/v1/product-shelves/categories
    # 2. This returns a list of categories
    # 3. Loop through the list of categories and use the ID to get the subcategories using the endpoint https://api.ah.nl/mobile-services/v1/product-shelves/categories/{id}/sub-categories. 
    # This returns the category itself and a list of children.
    # 4. Recursively do this until there are no more children.

    categories = db_handler.get_categories()
    if not categories:
        connector = AHConnector()
        categories = connector.get_categories()
        result = []
        categories = get_categories(categories, result=result)
        # db_handler.add_categories(categories)
        print(result)


# pickle the categories to a file
    # with open("categories.pickle", "wb") as f:
    #     pickle.dump(categories, f)


    receipts = [Receipt(receipt) for receipt in fetch_receipts() if db_handler.find_receipt(receipt["transactionId"]) is None]

    new_receipts_count = 0
    for receipt in receipts:
        new_receipts_count += 1
        location = receipt.location
        dbLocation = db_handler.find_location(location.name)
        if not dbLocation:
            dbLocation = db_handler.add_location(location)
        dbReceipt = db_handler.add_receipt(receipt, dbLocation.id)   
        db_handler.add_products(receipt.products, dbReceipt.id)
        db_handler.add_discounts(receipt.discounts["discounts"], dbReceipt.id)
        categories = receipt.get_categories()
        db_handler.add_categories(categories)
        db_handler.set_categories_for_products(receipt.products)

    db_handler.close()
    log.info(f"Added {new_receipts_count} new receipts to the database.")

if __name__ == "__main__":
    main()