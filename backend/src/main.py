import logging
import os

from database.DbHandler import DbHandler
from ah_api import fetch_receipts
from config import Config
from classes.Receipt import Receipt
from previous_bought import fetch_previous_bought
from products import fetch_products

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    level=logging.INFO,
    handlers=[logging.FileHandler("grocitrack.log"), logging.StreamHandler()],
)
log = logging.getLogger(__name__)
config = Config()


def main():
    log.info("Connecting to database")
    db_handler = DbHandler()
    log.info("Connected to database.")

    if not db_handler.get_ah_produts():
        if os.path.exists("backend/src/database/ah_products.sql"):
            log.info("Creating products table from SQL file")
            db_handler.execute_sql_file("backend/src/database/ah_products.sql")
            log.info("Created products table from SQL file")
        else:
            log.info("Fetching all products from AH API")
            all_ah_products = fetch_products()
            db_handler.add_ah_products(all_ah_products)
            log.info("Fetched products from AH API")

    if not db_handler.get_categories():
        if os.path.exists("backend/src/database/categories.sql"):
            log.info("Creating categories table from SQL file")
            db_handler.execute_sql_file("backend/src/database/categories.sql")
            db_handler.execute_sql_file("backend/src/database/categories_hierarchy.sql")
            log.info("Created categories table from SQL file")

    log.info("Fetching previously bought products")
    previous_products = fetch_previous_bought()
    db_handler.add_prev_products(previous_products)

    log.info("Fetching receipts")
    receipts_result = fetch_receipts()
    receipts = [
        Receipt(receipt)
        for receipt in receipts_result
        if db_handler.find_receipt(receipt["transactionId"]) is None
    ]
    log.info(f"Found {len(receipts)} new receipts.")
    receipts_processed = 0
    for receipt in receipts:
        log.info(f"Processing receipt {receipt.transaction_id} from {receipt.datetime}")
        receipt.set_details()
        if receipt.is_empty():
            log.debug(f"Receipt {receipt.transaction_id} is empty.")
            dbLocation = db_handler.find_location(receipt.location.name)
            if not dbLocation:
                dbLocation = db_handler.add_location(receipt.location)
            db_handler.add_receipt(receipt, dbLocation.id)
            continue
        location = receipt.location
        dbLocation = db_handler.find_location(location.name)
        if not dbLocation:
            dbLocation = db_handler.add_location(location)
        dbReceipt = db_handler.add_receipt(receipt, dbLocation.id)
        log.debug(f"Adding products from receipt {receipt.transaction_id}")
        db_handler.add_products(receipt.products, dbReceipt.id)
        log.debug(f"Adding discounts from receipt {receipt.transaction_id}")
        db_handler.add_discounts(receipt.discounts["discounts"], dbReceipt.id)
        log.debug(f"Setting product categories for receipt {receipt.transaction_id}")
        db_handler.set_categories_for_products(receipt.products)
        receipts_processed += 1
        log.info(f"Processed {receipts_processed}/{len(receipts)} receipts.")

    db_handler.close()
    log.info(
        f"Added {receipts_processed} new receipts to the database. {len(receipts) - receipts_processed} receipts were empty."
    )


if __name__ == "__main__":
    main()
