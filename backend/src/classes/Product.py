class Product:
    def __init__(self, quantity: float=None, unit: str=None, name: str=None, price: float=None, total_price: float=None, indicator: str=None):
        self.quantity = quantity
        self.unit = unit
        self.name = name
        self.price = price
        self.total_price = total_price
        self.indicator = indicator

    def __repr__(self):
        return f"Product(quantity={self.quantity}, unit={self.unit}, description={self.name}, price={self.price}, total_price={self.total_price}, indicator={self.indicator})"
