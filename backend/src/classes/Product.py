from supermarktconnector.ah import AHConnector
import pandas as pd
import re
from math import isnan


class Product:
    _connector = AHConnector()

    def __init__(self, quantity: float=None, unit: str=None, description: str=None, price: float=None, total_price: float=None, indicator: str=None):
        self.quantity = quantity
        self.unit = unit
        self.description = description
        self.name = None
        self.product_id = None
        self.categories = None
        self.price = price
        self.total_price = total_price
        self.indicator = indicator
        self.potential_products = None
        self._set_details()


    @property
    def connector(self):
        return type(self)._connector


    def _set_details(self):
        """Fetches and sets the details of the product."""
        if "statiegeld" in self.description.lower():
            return
        result = self.connector.search_products(query=self.description, size=200, page=0)
        df = pd.DataFrame(result["products"], columns=["webshopId", "title", "unitPriceDescription", "priceBeforeBonus", "mainCategory", "subCategory", "brand", "shopType"])
        df["unitPriceDescription"] = df["unitPriceDescription"].apply(self._clean_unit_price_description)
        product_not_found = False
        multiple_products_found = False
        if self.unit and self.unit.lower() == "kg":
            filtered_rows = df[df["unitPriceDescription"] == self.price]
        elif self.quantity == 1:
            filtered_rows = df[df["priceBeforeBonus"] == self.total_price]
        else:
            filtered_rows = df[df["priceBeforeBonus"] == self.price]
        
        length = filtered_rows.shape[0]
        if length == 0:
            row = df.iloc[0]
            product_not_found = True
        elif length == 1:
            row = filtered_rows.iloc[0]
        else:
            row = filtered_rows.iloc[0]
            multiple_products_found = True
            self.potential_products = filtered_rows
        
        product_details = self.connector.get_product_details(row["webshopId"])
        category_details = self.connector.get_product_category_details(product_details)
        if product_not_found or multiple_products_found:
            self.name = None
            self.product_id = None
        else:
            self.name = row["title"]
            self.product_id = row["webshopId"]
        categories = self._get_categories(category_details, row["webshopId"], row["subCategory"])
        self.categories = " > ".join(categories)


    def _get_categories(self, category_details: dict, product_id: int, product_subcategory: str) -> list:
        """Gets the categories of the product.

        Args:
            category_details (dict): The category details of the product.

        Returns:
            list: The categories of the product.
        """
        cards = category_details["cards"]
        card = None
        for c in cards:
            if product_id in c["products"]:
                card = c
                break
        if not card:
            # TODO: Check if the subcategory is in the categories
            card = cards[0]
        product = card["products"][0]
        taxonomies = product["taxonomies"]
        taxonomy_names = [taxonomy["name"] for taxonomy in taxonomies]
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
        return f"Product(quantity={self.quantity}, unit={self.unit}, name={self.name}, price={self.price}, total_price={self.total_price}, indicator={self.indicator})"
