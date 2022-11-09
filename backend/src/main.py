from sqlalchemy.orm import sessionmaker
from database.db import DbReceipt, DbProduct, DbDiscount, DbLocation, engine
from database.db_handler import DbHandler
from ah_api import fetch_receipts
from config import Config
from classes.Receipt import Receipt

config = Config()


def main():
    receipts = [Receipt(receipt) for receipt in fetch_receipts()]

    db_handler = DbHandler()
    new_receipts_count = 0
    for receipt in receipts:
        if db_handler.find_receipt(receipt.transaction_id):
            continue
        new_receipts_count += 1
        location = receipt.location
        dbLocation = db_handler.find_location(location.name)
        if not dbLocation:
            dbLocation = db_handler.add_location(location)
        dbReceipt = db_handler.add_receipt(receipt, dbLocation.id)   
        db_handler.add_products(receipt.products, dbReceipt.id)
        db_handler.add_discounts(receipt.discounts["discounts"], dbReceipt.id)
    db_handler.close()
    print(f"Found {len(receipts)} receipts, added {new_receipts_count} new receipts to the database.")


if __name__ == "__main__":
    main()