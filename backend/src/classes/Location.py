class Location:
    def __init__(
        self,
        name: str = None,
        address: str = None,
        house_number: str = None,
        postal_code: str = None,
        city: str = None,
    ):
        self.name = name
        self.address = address
        self.house_number = house_number
        self.postal_code = postal_code
        self.city = city

    def __repr__(self):
        return f"Location(name={self.name}, address={self.address}, house_number={self.house_number}, postal_code={self.postal_code}, city={self.city})"
