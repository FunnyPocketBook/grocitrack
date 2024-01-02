from supermarktconnector.ah import AHConnector
import pandas as pd
import re
from math import isnan


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
        self._set_details()

    @property
    def connector(self):
        return type(self)._connector

    # def _match_product(self, products: list[DbAHProducts]):

    def _set_details(self):
        """Fetches and sets the details of the product."""
        from database.DbHandler import DbHandler

        db_handler = DbHandler()

        if (
            "statiegeld" in self.description.lower()
            or "airmiles" in self.description.lower()
        ):
            return
        result2 = self.connector.search_products(
            query=self.description, size=15, page=0
        )
        result = db_handler.search_product(input=self.description)
        if result["products"] == []:
            # TODO: create function to match product
            self.product_not_found = True
            return
        df = pd.DataFrame(result["products"], columns=result["products"][0].keys())
        if "unitPriceDescription" in df.columns:
            df["unitPriceDescription"] = df["unitPriceDescription"].apply(
                self._clean_unit_price_description
            )
        else:
            df["unitPriceDescription"] = None
        if self.unit and self.unit.lower() == "kg":
            filtered_rows = df[df["unitPriceDescription"] == self.price]
        elif "priceBeforeBonus" in df.columns:
            if self.quantity == 1:
                filtered_rows = df[df["priceBeforeBonus"] == self.total_price]
            else:
                filtered_rows = df[df["priceBeforeBonus"] == self.price]
        else:
            filtered_rows = df[df["currentPrice"] == self.price]

        length = filtered_rows.shape[0]
        if length == 0:
            row = df.iloc[0]
            self.potential_products = result["products"]
            self.product_not_found = True
        elif length == 1:
            row = filtered_rows.iloc[0]
        else:
            row = filtered_rows.iloc[0]
            self.potential_products = filtered_rows.to_dict(orient="records")
            self.product_not_found = True

        if self.potential_products:
            for item in self.potential_products:
                for key in item:
                    if isinstance(item[key], float) and isnan(item[key]):
                        item[key] = None

        self.name = row["title"]
        self.product_id = str(row["webshopId"])
        self.category = db_handler.find_category_by_name(row["subCategory"]).taxonomy_id

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
