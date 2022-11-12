from database.db import DbReceipt, DbProduct, DbDiscount, DbLocation, DbCategory, DbCategoryHierarchy, engine
from classes.Receipt import Receipt
from classes.Location import Location
from classes.Product import Product
from classes.Discount import Discount
from sqlalchemy.orm import sessionmaker
import pickle

class DbHandler:
    """Class for handling database operations
    
    Attributes:
        _session (Session): The database session
        
    Methods:
        find_receipt(transaction_id: str) -> DbReceipt

        find_location(name: str) -> DbLocation

        add_location(location: Location) -> DbLocation

        add_receipt(receipt: Receipt, location_id: int) -> DbReceipt

        add_product(product: Product, receipt_id: int) -> DbProduct

        add_products(products: list[Product], receipt_id: int)

        add_discount(discount: Discount, receipt_id: int) -> DbDiscount

        add_discounts(discounts: list[Discount], receipt_id: int)

        close()"""
    def __init__(self):
        self._session = sessionmaker(bind=engine)()


    def find_receipt(self, transaction_id: str) -> DbReceipt:
        """Finds a receipt by transaction_id
        
        Args:
            transaction_id (str): The transaction_id of the receipt
            
        Returns:
            DbReceipt: The receipt with the given transaction_id"""
        return self._session.query(DbReceipt).filter_by(transaction_id=transaction_id).first()


    def find_location(self, name: str) -> DbLocation:
        """Finds a location by name
        
        Args:
            name (str): The name of the location
        
        Returns:
            DbLocation: The location with the given name"""
        return self._session.query(DbLocation).filter_by(name=name).first()


    def find_category(self, name: str) -> DbCategory:
        """Finds a category by name

        Args:
            name (str): The name of the category

        Returns:
            DbCategory: The category with the given name"""
        return self._session.query(DbCategory).filter_by(name=name).first()


    def add_location(self, location: Location) -> DbLocation:
        """Adds a location to the database

        Args:
            location (Location): The location to add

        Returns:    
            DbLocation: The added location"""
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


    def add_receipt(self, receipt: Receipt, location_id: int) -> DbReceipt:
        """Adds a receipt to the database

        Args:
            receipt (Receipt): The receipt to add
            location_id (int): The id of the location

        Returns:
            DbReceipt: The added receipt"""
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

    
    def add_category(self, category: str, parent_id: int = None) -> DbCategory:
        """Adds a category to the database

        Args:
            category (str): The name of the category
            parent_id (int, optional): The id of the parent category. Defaults to None.

        Returns:
            DbCategory: The added category"""
        dbCategory = DbCategory(name=category)
        self._session.add(dbCategory)
        self._session.commit()
        dbCategoryHierarchy = DbCategoryHierarchy(parent_id=parent_id, child_id=dbCategory.id)
        self._session.add(dbCategoryHierarchy)
        self._session.commit()
        return dbCategory


    def add_product(self, product: Product, receipt_id: int) -> DbProduct:
        """Adds a product to the database
        
        Args:
            product (Product): The product to add
            receipt_id (int): The id of the receipt
            
        Returns:
            DbProduct: The added product"""
        dbProduct = DbProduct(
            description=product.description,
            name=product.name,
            receipt=receipt_id,
            quantity=product.quantity,
            unit=product.unit,
            price=product.price,
            total_price=product.total_price,
            categories=product.categories,
        )
        self._session.add(dbProduct)
        self._session.commit()
        return dbProduct


    def add_products(self, products: list[Product], receipt_id: int):
        """Adds a list of products to the database
        
        Args:
            products (list[Product]): The list of products to add
            receipt_id (int): The id of the receipt"""
        for product in products:
            self.add_product(product, receipt_id)


    def add_discount(self, discount: Discount, receipt_id: int) -> DbDiscount:
        """Adds a discount to the database

        Args:
            discount (Discount): The discount to add
            receipt_id (int): The id of the receipt

        Returns:
            DbDiscount: The added discount"""
        dbDiscount = DbDiscount(
            receipt=receipt_id,
            type=discount.type,
            description=discount.description,
            amount=discount.amount,
        )
        self._session.add(dbDiscount)
        self._session.commit()
        return dbDiscount

    
    def add_discounts(self, discounts: list[Discount], receipt_id: int):
        """Adds a list of discounts to the database

        Args:
            discounts (list[Discount]): The list of discounts to add
            receipt_id (int): The id of the receipt"""
        for discount in discounts:
            self.add_discount(discount, receipt_id)

    def close(self):
        """Closes the session"""
        self._session.close()

    def __del__(self):
        self.close()