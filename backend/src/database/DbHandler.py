from database.db import DbReceipt, DbProduct, DbDiscount, DbLocation, engine
from sqlalchemy.orm import sessionmaker
import pickle

class DbHandler:
    def __init__(self):
        self._session = sessionmaker(bind=engine)()


    def find_receipt(self, transaction_id):
        return self._session.query(DbReceipt).filter_by(transaction_id=transaction_id).first()


    def find_location(self, name):
        return self._session.query(DbLocation).filter_by(name=name).first()


    def add_location(self, location):
        dbLocation = DbLocation(
            name=location.name,
            address=location.address,
            house_number=location.house_number,
            city=location.city,
            postal_code=location.postal_code,
        )
        self._session.add(dbLocation)
        self._session.commit()
        return dbLocation


    def add_receipt(self, receipt, location_id):
        dbReceipt = DbReceipt(
            transaction_id=receipt.transaction_id,
            datetime=receipt.datetime,
            location=location_id,
            total_price=receipt.total,
            total_discount=receipt.discounts["total_discount"],
            pickle=pickle.dumps(receipt),
        )
        self._session.add(dbReceipt)
        self._session.commit()
        return dbReceipt


    def add_product(self, product, receipt_id):
        dbProduct = DbProduct(
            name=product.name,
            receipt=receipt_id,
            quantity=product.quantity,
            unit=product.unit,
            price=product.price,
            total_price=product.total_price,
        )
        self._session.add(dbProduct)
        self._session.commit()
        return dbProduct


    def add_products(self, products, receipt_id):
        for product in products:
            self.add_product(product, receipt_id)


    def add_discount(self, discount, receipt_id):
        dbDiscount = DbDiscount(
            receipt=receipt_id,
            type=discount.type,
            description=discount.description,
            amount=discount.amount,
        )
        self._session.add(dbDiscount)
        self._session.commit()
        return dbDiscount

    
    def add_discounts(self, discounts, receipt_id):
        for discount in discounts:
            self.add_discount(discount, receipt_id)

    def close(self):
        self._session.close()

    def __del__(self):
        self.close()