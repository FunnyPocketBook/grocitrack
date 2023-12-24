from database.db_legacy import DbReceipt, DbProduct, DbDiscount, DbLocation, DbCategory, DbCategoryHierarchy, DbCategoryProduct, engine
from classes.Receipt import Receipt
from classes.Location import Location
from classes.Product import Product
from classes.Discount import Discount
from classes.Category import Category
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
import pickle
import logging

log = logging.getLogger(__name__)

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
    def __init__(self, _engine=engine):
        self._engine = _engine
        self._session = sessionmaker(bind=self._engine)()

    
    def execute_sql_file(self, file_path: str):
        """Executes a SQL file
        
        Args:
            file_path (str): The path to the SQL file"""
        with open(file_path, "r") as file:
            script = file.read()
        statements = script.split(";")
        for statement in statements:
            if statement.strip():
                self._engine.execute(text(statement))


    def find_receipt(self, transaction_id: str) -> DbReceipt:
        """Finds a receipt by transaction_id
        
        Args:
            transaction_id (str): The transaction_id of the receipt
            
        Returns:
            DbReceipt: The receipt with the given transaction_id"""
        return self._session.query(DbReceipt).filter_by(transaction_id=transaction_id).first()

    
    def find_product(self, product: Product) -> DbProduct:
        """Finds a product in the database

        Args:
            product (Product): The product to find

        Returns:
            DbProduct: The found product"""
        return self._session.query(DbProduct).filter_by(name=product.name).first()


    def find_location(self, name: str) -> DbLocation:
        """Finds a location by name
        
        Args:
            name (str): The name of the location
        
        Returns:
            DbLocation: The location with the given name"""
        return self._session.query(DbLocation).filter_by(name=name).first()


    def find_category(self, taxonomy_id: str) -> DbCategory:
        """Finds a category by taxonomy ID

        Args:
            taxonomy_id (str): The taxonomy ID of the category

        Returns:
            DbCategory: The category with the given name"""
        return self._session.query(DbCategory).filter_by(taxonomy_id=taxonomy_id).first()
    

    def get_receipts(self) -> list[DbReceipt]:
        """Gets all receipts from the database
        
        Returns:
            list[DbReceipt]: The list of receipts"""
        return self._session.query(DbReceipt).all()
    
    def get_receipt(self, receipt_id: int) -> DbReceipt:
        """Gets a receipt from the database
        
        Args:
            receipt_id (int): The ID of the receipt
        
        Returns:
            DbReceipt: The receipt with the given ID"""
        return self._session.query(DbReceipt).get(receipt_id)
    

    def get_products(self) -> list[DbProduct]:
        """Gets all products from the database
        
        Returns:
            list[DbProduct]: The list of products"""
        return self._session.query(DbProduct).all()
        

    def get_categories(self) -> list[DbCategory]:
        """Gets all categories from the database

        Returns:
            list[DbCategory]: The list of categories"""
        return self._session.query(DbCategory).all()
    
    def get_categories_hierarchy(self) -> list[DbCategoryHierarchy]:
        """Gets all category hierarchies from the database

        Returns:
            list[DbCategoryHierarchy]: The list of category hierarchies"""
        return self._session.query(DbCategoryHierarchy).all()
    
    def get_categories_products(self) -> list[DbCategoryProduct]:
        """Gets all category products from the database

        Returns:
            list[DbCategoryProduct]: The list of category products"""
        return self._session.query(DbCategoryProduct).all()
    

    def get_discounts(self) -> list[DbDiscount]:
        """Gets all discounts from the database

        Returns:
            list[DbDiscount]: The list of discounts"""
        return self._session.query(DbDiscount).all()
    
    def get_locations(self) -> list[DbLocation]:
        """Gets all locations from the database

        Returns:
            list[DbLocation]: The list of locations"""
        return self._session.query(DbLocation).all()
    

    def get_category_product(self, product_id: str, taxonomy_id: str) -> list[DbCategoryProduct]:
        """Gets all category products from the database

        Args:
            product_id (str): The ID of the product
            taxonomy_id (str): The taxonomy ID of the category

        Returns:
            list[DbCategoryProduct]: The list of category products"""
        return self._session.query(DbCategoryProduct).filter_by(product_id=product_id, taxonomy_id=taxonomy_id).all()
    

    def get_category_hierarchy_parents(self, taxonomy_id: str, result: list[DbCategory]) -> list[DbCategory]:
        """Gets all parent categories based on taxonomy_id from the database

        Args:
            taxonomy_id (str): The taxonomy ID of the category
            result (list[DbCategory]): The list of categories to add to (recursive)

        Returns:
            list[DbCategory]: The list of categories"""
        dbCategory = self.find_category(taxonomy_id)
        if dbCategory is None:
            log.error(f"Category \"{taxonomy_id}\" not found")
            # TODO: get new category from API and insert into DB
            return None
        result.append(dbCategory)
        dbCategoryHierarchies = self._session.query(DbCategoryHierarchy).filter_by(child=taxonomy_id).all()
        for dbCategoryHierarchy in dbCategoryHierarchies:
            self.get_category_hierarchy_parents(dbCategoryHierarchy.parent, result)
        return result
        

    
    def set_categories_for_products(self, products: list[Product]) -> list[DbCategoryProduct]:
        """Sets the categories for the products in the database

        Args:
            products (list[Product]): The list of products
            
        Returns:
            list[DbCategoryProduct]: The list of added category products"""
        categoryProducts = []
        for product in products:
            dbCategoryProducts = self.set_categories_for_product(product)
            if dbCategoryProducts is not None:
                categoryProducts.append(dbCategoryProducts)
        return categoryProducts


    def set_categories_for_product(self, product: Product) -> DbCategoryProduct:
        """Sets the categories for a product into CategoryProduct table

        Args:
            product (Product): The product to set the categories for"""
        dbProduct = self.find_product(product)
        if dbProduct is None:
            log.error(f"Product \"{product.name}\" not found")
            return None
        if product.category is None:
            log.error(f"Product \"{product.name}\" has no categories")
            return None
        dbCategories = self.get_category_hierarchy_parents(product.category, [])
        if dbCategories is None:
            log.error(f"Product \"{product.name}\" has no categories")
            return None
        for dbCategory in dbCategories:
            dbCategoryProduct = self.get_category_product(dbProduct.product_id, dbCategory.taxonomy_id)
            if dbCategoryProduct:
                continue
            dbCategoryProduct = DbCategoryProduct(
                product_id=dbProduct.product_id,
                taxonomy_id=dbCategory.taxonomy_id,
            )
            self._session.add(dbCategoryProduct)
            self._session.flush()
            log.debug(f"Added category \"{dbCategory.name}\" to product \"{product.name}\"")
        self._session.commit()
        return dbCategories

    
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
        log.info(f"Added receipt from {receipt.datetime} to database")
        return dbReceipt
    

    def add_category(self, category: Category, parent: DbCategory=None) -> DbCategory:
        """Adds a category to the database

        Args:
            category (Category): The category to add
            parent (DbCategory, optional): The parent category. Defaults to None.

        Returns:
            DbCategory: The added category"""
        dbCategory = self.find_category(category.taxonomy_id)
        if dbCategory is None:
            dbCategory = DbCategory(
                name=category.name,
                slug=category.slug,
                taxonomy_id=category.taxonomy_id,
            )
            self._session.add(dbCategory)
            self._session.commit()

            if parent is not None:               
                dbCategoryHierarchy = DbCategoryHierarchy(
                    parent=parent.taxonomy_id,
                    child=dbCategory.taxonomy_id,
                )
                self._session.add(dbCategoryHierarchy)
                self._session.commit()
            
            if category.children is not None:
                for child in category.children:
                    self.add_category(child, dbCategory)

            log.info(f"Added category \"{category.name}\" to database")
        else:
            log.info(f"Category \"{category.name}\" already exists in database")
        return dbCategory
    




    # def add_categories(self, categories: dict) -> list[DbCategory]:
    #     """Adds categories to the database recursively. 
    #     If a category already exists, it will not be added again.

    #     Args:
    #         categories (dict): The categories to add
            
    #     Returns:
    #         list[DbCategory]: The added categories"""
    #     dbCategories = []
    #     for category in categories:
    #         dbCategories.append(self.add_category(categories[category]))
    #     return dbCategories

    # def add_category(self, categories: dict) -> DbCategory:
    #     """Adds a category to the database

    #     Args:
    #         name (str): The name of the category
    #         subcategories (list[str]): The subcategories of the category
            
    #     Returns:
    #         DbCategory: The added category"""
    #     category = categories["category"]
    #     dbCategory = self.find_category(category.name)
    #     if dbCategory is None:
    #         dbCategory = DbCategory(name=category.name, taxonomy_id=category.taxonomy_id)
    #         self._session.add(dbCategory)
    #         self._session.flush()
    #     subcategories = categories["subcategories"]
    #     for subcategory in subcategories:
    #         self.add_category(subcategories[subcategory])
    #         dbSubcategory = self.find_category(subcategories[subcategory]["category"].name)
    #         dbCategoryHierarchy = DbCategoryHierarchy(
    #             parent=dbCategory.id,
    #             child=dbSubcategory.id,
    #         )
    #         self._session.add(dbCategoryHierarchy)
    #         self._session.flush()
    #     self._session.commit()
    #     return dbCategory
        
        


    def add_product(self, product: Product, receipt_id: int) -> DbProduct:
        """Adds a product to the database
        
        Args:
            product (Product): The product to add
            receipt_id (int): The id of the receipt
            
        Returns:
            DbProduct: The added product"""
        dbProduct = DbProduct(
            product_id=product.product_id,
            description=product.description,
            name=product.name,
            receipt=receipt_id,
            quantity=product.quantity,
            unit=product.unit,
            price=product.price,
            total_price=product.total_price,
            potential_products=product.potential_products,
            product_not_found=product.product_not_found,
        )
        self._session.add(dbProduct)
        self._session.commit()
        log.debug(f"Added product \"{product.name}\" to database")
        return dbProduct


    def add_products(self, products: list[Product], receipt_id: int) -> list[DbProduct]:
        """Adds a list of products to the database
        
        Args:
            products (list[Product]): The list of products to add
            receipt_id (int): The id of the receipt
            
        Returns:
            list[DbProduct]: The added products"""
        dbProducts = []
        for product in products:
            dbProducts.append(self.add_product(product, receipt_id))
        return dbProducts

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
        log.debug(f"Added discount \"{discount.description}\" to database")
        return dbDiscount

    
    def add_discounts(self, discounts: list[Discount], receipt_id: int) -> list[DbDiscount]:
        """Adds a list of discounts to the database

        Args:
            discounts (list[Discount]): The list of discounts to add
            receipt_id (int): The id of the receipt
            
        Returns:
            list[DbDiscount]: The added discounts"""
        DbDiscounts = []
        for discount in discounts:
            DbDiscounts.append(self.add_discount(discount, receipt_id))
        return DbDiscounts

    def close(self):
        """Closes the session"""
        self._session.close()

    def __del__(self):
        self.close()