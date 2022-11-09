from datetime import datetime
import requests
from classes.Location import Location
from classes.Product import Product
from classes.Discount import Discount
from util import string_to_float, parse_quantity
from ah_api import update_tokens
from config import Config

config = Config()

class Receipt:
    RECEIPT_DETAILS_URL = "https://api.ah.nl/mobile-services/v2/receipts/{transaction_id}"

    def __init__(self, receipt):
        self.transaction_id = receipt["transactionId"]
        self.datetime = datetime.strptime(receipt["transactionMoment"], "%Y-%m-%dT%H:%M:%SZ")
        self.receipt_details = self._get_receipt_details()
        self.location = self._get_location(receipt["storeAddress"])
        self.total = receipt["total"]["amount"]["amount"]
        self.products = self._get_products()
        self.discounts = self._get_discounts()


    def _get_receipt_details(self) -> list:
        """Fetch the details of a receipt from the API."""
        url = self.RECEIPT_DETAILS_URL.format(transaction_id=self.transaction_id)
        response = requests.get(url, headers={"Authorization": f"Bearer {config.get('api')['access_token']}"})
        if response.status_code == 401:
            update_tokens()
            response = requests.get(url, headers={"Authorization": f"Bearer {config.get('api')['access_token']}"})
        response.raise_for_status()
        return response.json()["receiptUiItems"]

    def _get_location(self, store):
        """Set the store location of the receipt."""
        return Location(
            name=self.receipt_details[1]["value"],
            address=store["street"],
            house_number=store["houseNumber"],
            postal_code=store["postalCode"],
            city=store["city"],
        )


    def _get_products(self) -> list:
        receipt_rows = self.receipt_details

        # Remove all elements before "bonuskaart" (and that element itself) and after "subtotaal" to get only the products that have been purchased (without discounts etc.)
        before_index = next((index for (index, d) in enumerate(receipt_rows) if d["type"].lower() == "product" and d["description"].lower() == "bonuskaart"), None)
        after_index = next((index for (index, d) in enumerate(receipt_rows) if d["type"].lower() == "subtotal" and d["text"].lower() == "subtotaal"), None)
        product_rows = receipt_rows[before_index + 1:after_index]

        # remove all entires don't have the type "product"
        product_rows = [item for item in product_rows if item["type"].lower() == "product"]
        products = self._parse_products(product_rows)
        return products


    def _get_discounts(self) -> dict:
        receipt_rows = self.receipt_details

        # Remove all elements before "subtotaal" (and that element itself) and after "uw voordeel" to get only the discounts that were applied
        before_index = next((index for (index, d) in enumerate(receipt_rows) if d["type"].lower() == "subtotal" and d["text"].lower() == "subtotaal"), None)
        after_index = next((index for (index, d) in enumerate(receipt_rows) if d["type"].lower() == "total" and d["label"].lower() == "uw voordeel"), None)
        product_rows = receipt_rows[before_index + 1:after_index]

        # remove all entires don't have the type "product", as all discounts also have the type product
        product_rows = [item for item in product_rows if item["type"].lower() == "product"]
        discounts = {"discounts": [], "total_discount": 0.0}
        for row in product_rows:
            discount_amount = abs(string_to_float(row["amount"]))
            discount = Discount(row["quantity"], row["description"], discount_amount)
            discounts["discounts"].append(discount)
            discounts["total_discount"] += discount_amount
        return discounts
    
    
    def _parse_products(self, items: list) -> list:
        """Parse the products from the API response.
        
        Args:
            items (list): The items from the API response.
            
        Returns:
            list: A list of Product objects.
        """
        products = []
        for row in items:
            if "statiegeld" in row["description"].lower():
                product = Product(1.0, None, row["description"], None, string_to_float(row["amount"]), None)
            else:
                quantity, unit = parse_quantity(row["quantity"])
                price = string_to_float(row["price"]) if "price" in row else None
                if row["indicator"] == "":
                    row["indicator"] = None
                amount = string_to_float(row["amount"])
                product = Product(quantity, unit, row["description"], price, amount, row["indicator"])
            products.append(product)
        return products


    def __repr__(self):
        return f"Receipt(transaction_id={self.transaction_id}, datetime={self.datetime}, location={self.location}, total={self.total}, products={self.products}, discounts={self.discounts})"
