class Category():
    """
    Category class
    
    Attributes:
        taxonomy_id (str): The id of the category
        name (str): The name of the category
        slug (str): The slugified name of the category
        parent (Category): The parent category
        children (list): The children categories
        images (list): The images of the category
    """
    def __init__(self, taxonomy_id: str=None, name: str=None, slug: str=None, parent: str=None, images: list=None):
        self.taxonomy_id = taxonomy_id
        self.name = name
        self.slug = slug
        self.parent = parent
        self.children = []
        self.images = images

    
    def add_child(self, child: "Category"):
        self.children.append(child)

    def set_parent(self, parent: "Category"):
        self.parent = parent

    def __repr__(self):
        return f"Category(name={self.name}, taxonomy_id={self.taxonomy_id}, slug={self.slug})"

    def __str__(self):
        return self.name

    # JSON serialization
    def __json__(self):
        return {
            "taxonomy_id": self.taxonomy_id,
            "name": self.name,
            "slug": self.slug
        }