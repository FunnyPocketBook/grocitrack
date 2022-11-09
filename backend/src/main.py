from sqlalchemy.orm import sessionmaker
from db import DbReceipt, DbProduct, DbDiscount, DbLocation, engine
from ah_api import fetch_receipts
from config import Config
from classes.Receipt import Receipt

config = Config()


def main():
    receipts = [Receipt(receipt) for receipt in fetch_receipts()]

    Session = sessionmaker(bind=engine)
    session = Session()
    new_receipts_count = 0
    for receipt in receipts:
        # if receipt is already in the database, skip it
        if session.query(DbReceipt).filter_by(transaction_id=receipt.transaction_id).first():
            continue
        new_receipts_count += 1
        # Create a new location
        location = receipt.location
        dbLocation = DbLocation(
            name=location.name,
            address=location.address,
            house_number=location.house_number,
            city=location.city,
            postal_code=location.postal_code,
        )
        # Add the location to the database if it doesn't exist yet
        existing_location = session.query(DbLocation).filter_by(name=location.name).first()
        if not existing_location:
            session.add(dbLocation)
            session.commit()
        # Create a new receipt
        dbReceipt = DbReceipt(
            transaction_id=receipt.transaction_id,
            datetime=receipt.datetime,
            location=dbLocation.id if not existing_location else existing_location.id,
            total_price=receipt.total,
            total_discount=receipt.discounts["total_discount"],
        )
        # Add the receipt to the session
        session.add(dbReceipt)
        session.commit()    
        # Add the products to the session
        for product in receipt.products:
            dbProduct = DbProduct(
                name=product.name,
                receipt=dbReceipt.id,
                quantity=product.quantity,
                unit=product.unit,
                price=product.price,
                total_price=product.total_price,
            )
            session.add(dbProduct)

        # Add the discounts to the session
        for discount in receipt.discounts["discounts"]:
            dbDiscount = DbDiscount(
                receipt=dbReceipt.id,
                type=discount.type,
                description=discount.description,
                amount=discount.amount,
            )
            session.add(dbDiscount)
        session.commit()
    session.close()
    print(f"Found {len(receipts)} receipts, added {new_receipts_count} new receipts to the database.")


if __name__ == "__main__":
    main()