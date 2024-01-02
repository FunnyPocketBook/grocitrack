import logging

from database.DbHandler import DbHandler
from ah_api import fetch_receipts
from config import Config
from classes.Receipt import Receipt
from previous_bought import fetch_previous_bought

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    level=logging.DEBUG,
    handlers=[logging.FileHandler("debug.log"), logging.StreamHandler()],
)
log = logging.getLogger(__name__)
config = Config()


def main():
    db_handler = DbHandler()

    previous_products = fetch_previous_bought()
    db_handler.add_prev_products(previous_products)

    receipts_result = fetch_receipts()
    receipts = [
        Receipt(receipt)
        for receipt in receipts_result
        if db_handler.find_receipt(receipt["transactionId"]) is None
    ]
    log.debug(f"Found {len(receipts)} new receipts.")
    for receipt in receipts:
        log.debug(
            f"Processing receipt {receipt.transaction_id} from {receipt.datetime}"
        )
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
        db_handler.add_products(receipt.products, dbReceipt.id)
        db_handler.add_discounts(receipt.discounts["discounts"], dbReceipt.id)
        db_handler.set_categories_for_products(receipt.products)

    db_handler.close()
    log.info(f"Added {len(receipts)} new receipts to the database.")


if __name__ == "__main__":
    main()
