from database.DbHandler_legacy import DbHandler
from database.DbHandler import DbHandler as DbHandler_postgres
import pickle
import math

db_handler = DbHandler()
db_handler_postgres = DbHandler_postgres()

categories = db_handler.get_categories()
categories_hierarchy = db_handler.get_categories_hierarchy()
categories_products = db_handler.get_categories_products()
discounts = db_handler.get_discounts()
locations = db_handler.get_locations()
products = db_handler.get_products()
receipts = db_handler.get_receipts()

for product in products:
    if product.potential_products:
        product.potential_products = pickle.loads(product.potential_products)
        for item in product.potential_products:
            for key in item:
                if isinstance(item[key], float) and math.isnan(item[key]):
                    item[key] = None
    else:
        product.potential_products = []

db_handler_postgres.add_all_locations(locations)
print("added locations")
db_handler_postgres.add_all_receipts(receipts)
print("added receipts")
db_handler_postgres.add_all_discounts(discounts)
print("added discounts")
db_handler_postgres.add_all_categories(categories)
print("added categories")
db_handler_postgres.add_all_categories_hierarchy(categories_hierarchy)
print("added categories hierarchy")
db_handler_postgres.add_all_categories_products(categories_products)
print("added categories products")
db_handler_postgres.add_all_products(products)
print("added products")
db_handler_postgres._session.commit()

print("done!")
