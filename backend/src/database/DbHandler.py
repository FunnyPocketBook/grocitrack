from util import translate
from database.setup import engine
from database.model import (
    DbAHProducts,
    DbPreviousProducts,
    DbReceipt,
    DbProduct,
    DbDiscount,
    DbLocation,
    DbCategory,
    DbCategoryHierarchy,
    DbCategoryProduct,
)
from classes.Product import Product
from classes.Receipt import Receipt
from classes.Location import Location
from classes.Discount import Discount
from classes.Category import Category
from sqlalchemy.orm import sessionmaker, aliased

import logging

from sqlalchemy import func, text, select

log = logging.getLogger(__name__)
logging.getLogger("connectionpool").setLevel(logging.WARNING)


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

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DbHandler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, _engine=engine):
        self._engine = _engine
        self._session = sessionmaker(bind=self._engine)()

    def execute_sql_file(self, file_path: str):
        """Executes a SQL file

        Args:
            file_path (str): The path to the SQL file"""
        with open(file_path, "r", encoding="utf8") as file:
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
        return (
            self._session.query(DbReceipt)
            .filter_by(transaction_id=transaction_id)
            .first()
        )

    def find_product(self, product: "Product") -> DbProduct:
        """Finds a product in the database

        Args:
            product (Product): The product to find

        Returns:
            DbProduct: The found product"""
        try:
            return (
                self._session.query(DbProduct)
                .filter_by(name=product.name, description=product.description)
                .first()
            )
        except Exception as e:
            log.error(f"Error finding product: {e}")
            return None

    def find_location(self, name: str) -> DbLocation:
        """Finds a location by name

        Args:
            name (str): The name of the location

        Returns:
            DbLocation: The location with the given name"""
        try:
            return self._session.query(DbLocation).filter_by(name=name).first()
        except Exception:
            return None

    def find_category(self, taxonomy_id: str) -> DbCategory:
        """Finds a category by taxonomy ID

        Args:
            taxonomy_id (str): The taxonomy ID of the category

        Returns:
            DbCategory: The category with the given name"""
        try:
            return (
                self._session.query(DbCategory)
                .filter_by(taxonomy_id=taxonomy_id)
                .first()
            )
        except Exception:
            return None

    def find_category_by_name(self, name: str) -> DbCategory:
        """Finds a category by name

        Args:
            name (str): The name of the category

        Returns:
            DbCategory: The category with the given name"""
        try:
            return self._session.query(DbCategory).filter_by(name=name).first()
        except Exception:
            return None

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

    def get_prev_products(self) -> list[DbPreviousProducts]:
        """Gets all previously bought products from the database

        Returns:
            list[DbPreviousProducts]: The list of previously bought products"""
        return self._session.query(DbPreviousProducts).all()

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

    def get_category_product(
        self, product_id: str, taxonomy_id: str
    ) -> list[DbCategoryProduct]:
        """Gets all category products from the database

        Args:
            product_id (str): The ID of the product
            taxonomy_id (str): The taxonomy ID of the category

        Returns:
            list[DbCategoryProduct]: The list of category products"""
        return (
            self._session.query(DbCategoryProduct)
            .filter_by(product_id=product_id, taxonomy_id=taxonomy_id)
            .all()
        )

    def search_product(
        self,
        input: str,
        threshold: float = 0.2,
        top_n_scores: int = 5,
        model: DbAHProducts | DbPreviousProducts = DbAHProducts,
    ) -> list:
        """Searches for a product in the database. The search is based on the similarity of the product name and the category name.

        Args:
            input (str): The input to search for
            threshold (float, optional): The similarity threshold. Defaults to 0.2.
            top_n_scores (int, optional): The number of top scores to return. Defaults to 5.

        Returns:
            list[DbAHProducts]: The list of products
        """
        max_score = func.greatest(
            func.similarity(model.title, func.lower(input)),
            func.similarity(model.sub_category, func.lower(input)),
        )
        # ScoredProducts Subquery
        scored_products_subq = (
            select(
                [
                    model.id,
                    max_score.label("max_score"),
                ]
            )
            .where(
                max_score > threshold,
            )
            .alias("scored_products")
        )

        top_n_scores_subq = (
            select([scored_products_subq.c.max_score])
            .group_by(scored_products_subq.c.max_score)
            .order_by(scored_products_subq.c.max_score.desc())
            .limit(top_n_scores)
            .alias("top_n_scores")
        )

        min_score_subq = select(
            [func.min(top_n_scores_subq.c.max_score).label("min_top_score")]
        ).alias("min_score")

        ScoredProducts = aliased(model, scored_products_subq)

        result_query = (
            self._session.query(scored_products_subq.c.max_score, model)
            .join(ScoredProducts, model.id == ScoredProducts.id)
            .filter(
                scored_products_subq.c.max_score
                >= select([min_score_subq.c.min_top_score]).scalar_subquery()
            )
        ).order_by(scored_products_subq.c.max_score.desc())

        result = result_query.all()
        return result

    def get_category_hierarchy_parents(
        self, taxonomy_id: str, result: list[DbCategory]
    ) -> list[DbCategory]:
        """Gets all parent categories based on taxonomy_id from the database

        Args:
            taxonomy_id (str): The taxonomy ID of the category
            result (list[DbCategory]): The list of categories to add to (recursive)

        Returns:
            list[DbCategory]: The list of categories"""
        dbCategory = self.find_category(taxonomy_id)
        if dbCategory is None:
            log.error(f'Category "{taxonomy_id}" not found')
            # TODO: get new category from API and insert into DB
            return None
        result.append(dbCategory)
        dbCategoryHierarchies = (
            self._session.query(DbCategoryHierarchy).filter_by(child=taxonomy_id).all()
        )
        for dbCategoryHierarchy in dbCategoryHierarchies:
            self.get_category_hierarchy_parents(dbCategoryHierarchy.parent, result)
        return result

    def set_categories_for_products(
        self, products: list["Product"]
    ) -> list[DbCategoryProduct]:
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

    def set_categories_for_product(self, product: "Product") -> DbCategoryProduct:
        """Sets the categories for a product into CategoryProduct table

        Args:
            product (Product): The product to set the categories for"""
        dbProduct = self.find_product(product)
        if dbProduct is None:
            log.error(
                f'Product "{product.description}" with name "{product.name}" not found'
            )
            return None
        if product.category is None:
            log.error(
                f'Product "{product.description}" with name "{product.name}" has no categories'
            )
            return None
        dbCategories = self.get_category_hierarchy_parents(product.category, [])
        if dbCategories is None:
            log.error(
                f'Product "{product.description}" with name "{product.name}" has no categories'
            )
            return None
        for dbCategory in dbCategories:
            dbCategoryProduct = self.get_category_product(
                dbProduct.product_id, dbCategory.taxonomy_id
            )
            if dbCategoryProduct:
                continue
            dbCategoryProduct = DbCategoryProduct(
                product_id=dbProduct.product_id,
                taxonomy_id=dbCategory.taxonomy_id,
            )
            self._session.add(dbCategoryProduct)
            self._session.flush()
            log.debug(f'Added category "{dbCategory.name}" to product "{product.name}"')
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
        )
        self._session.add(dbReceipt)
        self._session.commit()
        log.info(f"Added receipt from {receipt.datetime} to database")
        return dbReceipt

    def add_category(self, category: Category, parent: DbCategory = None) -> DbCategory:
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

            log.info(f'Added category "{category.name}" to database')
        else:
            if dbCategory.name != category.name:
                dbCategory.name = category.name
                dbCategory.slug = category.slug
                dbCategory.english = translate(category.name)
                self._session.commit()
                log.info(f'Updated category "{dbCategory.name}" to {category.name}')

            if category.children is not None:
                for child in category.children:
                    self.add_category(child, dbCategory)
        return dbCategory

    def add_product(self, product: "Product", receipt_id: int) -> DbProduct:
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
        log.debug(f'Added product "{product.name}" to database')
        return dbProduct

    def add_products(
        self, products: list["Product"], receipt_id: int
    ) -> list[DbProduct]:
        """Adds a list of products to the database

        Args:
            products (list[Product]): The list of products to add
            receipt_id (int): The id of the receipt

        Returns:
            list[DbProduct]: The added products"""
        dbProducts = [
            DbProduct(
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
            for product in products
        ]
        try:
            self._session.add_all(dbProducts)
            self._session.commit()
            log.debug(f"Added {len(dbProducts)} products to database")
        except Exception as e:
            log.error(f"Error adding products: {e}")
            self._session.rollback()
            raise

    def add_ah_product(self, product: DbAHProducts) -> DbAHProducts:
        """Adds a product to the database

        Args:
            product (DbAHProducts): The product to add

        Returns:
            DbAHProducts: The added product"""
        self._session.add(product)
        self._session.commit()
        log.debug(f'Added AH product "{product.title}" to database')
        return product

    def add_ah_products(self, products: list[DbAHProducts]) -> list[DbAHProducts]:
        """Adds a list of products to the database

        Args:
            products (list[DbAHProducts]): The list of products to add

        Returns:
            list[DbAHProducts]: The added products"""
        try:
            self._session.add_all(products)
            self._session.commit()
            log.debug(f"Added {len(products)} AH products to database")
        except Exception as e:
            log.error(f"Error adding products: {e}")
            self._session.rollback()
            raise
        return products

    def add_prev_product(self, product: DbPreviousProducts) -> DbPreviousProducts:
        """Adds a product to the database

        Args:
            product (DbPreviousProducts): The product to add

        Returns:
            DbPreviousProducts: The added product"""
        self._session.add(product)
        self._session.commit()
        log.debug(f'Added previous product "{product.title}" to database')
        return product

    def add_prev_products(
        self, products: list[DbPreviousProducts]
    ) -> list[DbPreviousProducts]:
        """Adds a list of products to the database

        Args:
            products (list[DbPreviousProducts]): The list of products to add

        Returns:
            list[DbPreviousProducts]: The added products"""
        existing_prev_products = self.get_prev_products()
        product_ids = [product.webshop_id for product in products]
        # if the ID of the product is already in the database but the name is different, replace the existing product with the new one
        # Go through existing_prev_products and check if the product ID is in the list of products to add
        # If it is, check if the name is different. If it is, replace the existing product with the new one
        for existing_prev_product in existing_prev_products:
            if existing_prev_product.webshop_id in product_ids:
                index = product_ids.index(existing_prev_product.webshop_id)
                product = products[index]
                if product.webshop_id == existing_prev_product.webshop_id and (
                    product.title != existing_prev_product.title
                    or product.current_price != existing_prev_product.current_price
                    or product.price_before_bonus
                    != existing_prev_product.price_before_bonus
                ):
                    self._session.delete(existing_prev_product)
                    self._session.add(product)
                    self._session.commit()
                    log.debug(f'Updated previous product "{product.title}"')

        existing_prev_product_ids = [
            prev_product.webshop_id for prev_product in existing_prev_products
        ]
        new_products = [
            product
            for product in products
            if product.webshop_id not in existing_prev_product_ids
        ]
        if len(new_products) == 0:
            log.debug("No new previous products to add")
            return []
        try:
            self._session.add_all(new_products)
            self._session.commit()
            log.debug(f"Added {len(new_products)} previous products to database")
        except Exception as e:
            log.error(f"Error adding products: {e}")
            self._session.rollback()
            raise
        return new_products

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
        log.debug(f'Added discount "{discount.description}" to database')
        return dbDiscount

    def add_discounts(
        self, discounts: list[Discount], receipt_id: int
    ) -> list[DbDiscount]:
        """Adds a list of discounts to the database

        Args:
            discounts (list[Discount]): The list of discounts to add
            receipt_id (int): The id of the receipt

        Returns:
            list[DbDiscount]: The added discounts"""
        dbDiscounts = []
        for discount in discounts:
            db_discount = DbDiscount(
                type=discount.type,
                description=discount.description,
                amount=discount.amount,
                receipt=receipt_id,
            )
            dbDiscounts.append(db_discount)

        try:
            self._session.add_all(dbDiscounts)
            self._session.commit()
            log.debug(f"Added {len(dbDiscounts)} discounts to database")
        except Exception as e:
            log.error(f"Error adding discounts: {e}")
            self._session.rollback()
            raise

        return dbDiscounts

    def add_all_categories(self, categories: list):
        dbCategories = [
            DbCategory(
                id=category.id,
                name=category.name,
                slug=category.slug,
                taxonomy_id=category.taxonomy_id,
                english=category.english,
            )
            for category in categories
        ]

        try:
            self._session.add_all(dbCategories)
            self._session.commit()
            log.debug(f"Added {len(dbCategories)} categories to database")
        except Exception as e:
            log.error(f"Error adding categories: {e}")
            self._session.rollback()
            raise

    def add_all_locations(self, locations: list):
        dbLocations = [
            DbLocation(
                id=location.id,
                name=location.name,
                address=location.address,
                house_number=location.house_number,
                city=location.city,
                postal_code=location.postal_code,
            )
            for location in locations
        ]
        try:
            self._session.add_all(dbLocations)
            self._session.commit()
            log.debug(f"Added {len(dbLocations)} locations to database")
        except Exception as e:
            log.error(f"Error adding locations: {e}")
            self._session.rollback()
            raise

    def add_all_products(self, products: list):
        dbProducts = [
            DbProduct(
                id=product.id,
                product_id=product.product_id,
                description=product.description,
                name=product.name,
                quantity=product.quantity,
                receipt=product.receipt,
                unit=product.unit,
                price=product.price,
                total_price=product.total_price,
                potential_products=product.potential_products,
                product_not_found=product.product_not_found,
            )
            for product in products
        ]
        try:
            self._session.add_all(dbProducts)
            self._session.commit()
            log.debug(f"Added {len(dbProducts)} products to database")
        except Exception as e:
            log.error(f"Error adding products: {e}")
            self._session.rollback()
            raise

    def add_all_discounts(self, discounts: list):
        for discount in discounts:
            dbDiscount = DbDiscount(
                id=discount.id,
                receipt=discount.receipt,
                type=discount.type,
                description=discount.description,
                amount=discount.amount,
            )
            self._session.add(dbDiscount)
        self._session.commit()

    def add_all_receipts(self, receipts: list):
        dbReceipts = [
            DbReceipt(
                id=receipt.id,
                transaction_id=receipt.transaction_id,
                datetime=receipt.datetime,
                total_price=receipt.total_price,
                total_discount=receipt.total_discount,
                location=receipt.location,
            )
            for receipt in receipts
        ]
        try:
            self._session.add_all(dbReceipts)
            self._session.commit()
            log.debug(f"Added {len(dbReceipts)} receipts to database")
        except Exception as e:
            log.error(f"Error adding receipts: {e}")
            self._session.rollback()
            raise

    def add_all_categories_hierarchy(self, categories_hierarchy: list):
        dbCategoryHierarchies = [
            DbCategoryHierarchy(
                id=category_hierarchy.id,
                parent=category_hierarchy.parent,
                child=category_hierarchy.child,
            )
            for category_hierarchy in categories_hierarchy
        ]
        try:
            self._session.add_all(dbCategoryHierarchies)
            self._session.commit()
            log.debug(
                f"Added {len(dbCategoryHierarchies)} category hierarchies to database"
            )
        except Exception as e:
            log.error(f"Error adding category hierarchies: {e}")
            self._session.rollback()
            raise

    def add_all_categories_products(self, categories_products: list):
        dbCategoryProducts = [
            DbCategoryProduct(
                id=category_product.id,
                product_id=category_product.product_id,
                taxonomy_id=category_product.taxonomy_id,
            )
            for category_product in categories_products
        ]
        try:
            self._session.add_all(dbCategoryProducts)
            self._session.commit()
            log.debug(f"Added {len(dbCategoryProducts)} category products to database")
        except Exception as e:
            log.error(f"Error adding category products: {e}")
            self._session.rollback()
            raise

    def close(self):
        """Closes the session"""
        self._session.close()

    def __del__(self):
        self.close()
