from supermarktconnector.ah import AHConnector
import pandas as pd
import re


class Product:
    _connector = AHConnector()

    def __init__(self, quantity: float=None, unit: str=None, description: str=None, price: float=None, total_price: float=None, indicator: str=None):
        self.quantity = quantity
        self.unit = unit
        self.description = description
        self.name = self._get_name()
        self.price = price
        self.total_price = total_price
        self.indicator = indicator

    
    def _set_details(self) -> str:
        """Fetch and set the details of the product."""
        result = self.connector.search_products(query=self.description, size=20, page=0)
        df = pd.DataFrame(result["products"], columns=["title", "unitPriceDescription", "priceBeforeBonus", "mainCategory", "subCategory", "subCategoryId", "brand", "shopType"])
        df["unitPriceDescription"] = df["unitPriceDescription"].apply(self._clean_unit_price_description)
        if self.unit.lower() == "kg":
            row = df[df["unitPriceDescription"] == self.price]
        elif self.quantity == 1:
            row = df[df["priceBeforeBonus"] == self.total_price]
        else:
            row = df[df["priceBeforeBonus"] == self.price]
    

    def _get_brand(self) -> str:
        """Get the brand of the product."""
        return self.connector.search_products(query=self.description, size=20, page=0)["products"][0]["brand"]


    def _clean_unit_price_description(self, unit_price_description: str) -> float:
        """Clean the unit price description."""
        regex = r"(\d+.\d+)"
        return float(re.find(regex, unit_price_description)[0])

    
    @property
    def connector(self):
        return type(self)._connector

    def __repr__(self):
        return f"Product(quantity={self.quantity}, unit={self.unit}, name={self.name}, price={self.price}, total_price={self.total_price}, indicator={self.indicator})"
