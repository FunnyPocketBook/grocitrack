from supermarktconnector.ah import AHConnector
import re
from math import isnan
from datetime import datetime

from database.model import DbAHProducts, DbPreviousProducts


class Product:
    _connector = AHConnector()

    def __init__(
        self,
        quantity: float = None,
        unit: str = None,
        description: str = None,
        price: float = None,
        total_price: float = None,
        indicator: str = None,
        datetime: datetime = None,
    ):
        self.quantity = quantity
        self.unit = unit
        self.description = description
        self.name = None
        self.product_id = None
        self.category = None
        self.price = price
        self.total_price = total_price
        self.indicator = indicator
        self.potential_products = None
        self.product_not_found = False
        self.datetime = datetime
        self._set_details()

    @property
    def connector(self):
        return type(self)._connector

    def _match_product(
        self, products: list[(float, DbAHProducts)]
    ) -> (DbAHProducts, bool):
        """Matches the product with the products in the database.

        Args:
            products (list[DbAHProducts]): The products to match.

        Returns:
            DbAHProducts: The matched product.
            bool: Whether the product is matched.

        """
        for similarity, product in products:
            if self.quantity == 1:
                if (
                    product.price_before_bonus == self.total_price
                    or product.current_price == self.total_price
                ):
                    return product, True
            else:
                if self.unit and self.unit.lower() == "kg":
                    unit_price = self._clean_unit_price_description(
                        product.unit_price_description
                    )
                    if unit_price == self.price:
                        return product, True
                else:
                    if (
                        product.current_price == self.price
                        or product.price_before_bonus == self.price
                    ):
                        return product, True
        return products[0][1], False

    def _set_details(self):
        """Fetches and sets the details of the product."""
        from database.DbHandler import DbHandler

        db_handler = DbHandler()

        if not self.quantity:
            return
        products = db_handler.search_product(
            input=self.description, model=DbPreviousProducts
        )
        if not products:
            products = db_handler.search_product(
                input=self.description, model=DbAHProducts
            )
        if not products:
            self.product_not_found = True
            return
        matched_product, is_matched = self._match_product(products)

        self.product_not_found = not is_matched
        self.name = matched_product.title
        self.product_id = matched_product.webshop_id
        self.category = db_handler.find_category_by_name(
            matched_product.sub_category
        ).taxonomy_id

    def _get_categories(
        self, category_details: dict, product_id: int, taxonomy: str
    ) -> list[dict]:
        """Gets the categories of the product.

        Args:
            category_details (dict): The category details of the product.
            product_id (int): The product id.
            taxonomy_id (int): The taxonomy id.

        Returns:
            list[dict]: The categories of the product.
        """
        cards = category_details["cards"]
        card = None
        for c in cards:
            if c["products"][0]["taxonomies"][-1]["name"] == taxonomy:
                card = c
            if c["id"] == product_id:
                card = c
                break
        if not card:
            card = cards[0]
        product = card["products"][0]
        taxonomy_names = product["taxonomies"]
        return taxonomy_names

    def _clean_unit_price_description(self, unit_price_description: str) -> float:
        """Cleans the unit price description.

        Args:
            unit_price_description (str): The unit price description.

        Returns:
            float: The cleaned unit price description."""
        if isinstance(unit_price_description, float) and isnan(unit_price_description):
            return None
        regex = r"(\d+.\d+)"
        return float(re.search(regex, unit_price_description).group(1))

    def __repr__(self):
        return f"Product(name={self.name}, product_id={self.product_id}, category={self.category}, price={self.price}, total_price={self.total_price}, indicator={self.indicator})"

    def __str__(self) -> str:
        return self.__repr__()
