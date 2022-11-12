class Category():
    def __init__(self, taxonomy_id: str=None, name: str=None):
        self.taxonomy_id = taxonomy_id
        self.name = name

    def __repr__(self):
        return f"Category(name={self.name}, taxonomy_id={self.taxonomy_id})"

    def __str__(self):
        return self.name

    # JSON serialization
    def __json__(self):
        return {
            "taxonomy_id": self.taxonomy_id,
            "name": self.name
        }