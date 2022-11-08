class Discount:
    def __init__(self, type: str=None, description: str=None, amount: float=None):
        self.type = type
        self.description = description
        self.amount = amount

    def __repr__(self):
        return f"Discount(description={self.description}, amount={self.amount})"