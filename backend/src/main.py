from database.DbHandler import DbHandler
from ah_api import fetch_receipts
from config import Config
from classes.Receipt import Receipt
import logging

logging.basicConfig(format="%(asctime)s [%(levelname)s] %(module)s: %(message)s", level=logging.INFO,
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ])
log = logging.getLogger(__name__)
config = Config()


def main():
    db_handler = DbHandler()
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