from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    ForeignKey,
    create_engine,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    LargeBinary,
    Boolean,
)
from config import Config


config = Config()


if config.get("database", "type") == "sqlite":
    engine = create_engine(f"sqlite:///{config.get('database')['name']}.db")
elif config.get("database", "type") == "mysql":
    engine = create_engine(
        f"mysql+pymysql://{config.get('database')['username']}:{config.get('database')['password']}@{config.get('database')['host']}/{config.get('database')['name']}"
    )
elif config.get("database", "type") == "postgresql" or config.get("database", "type") == "postgres":
    engine = create_engine(
        f"postgresql://{config.get('database')['username']}:{config.get('database')['password']}@{config.get('database')['host']}/{config.get('database')['name']}"
    )
else:
    raise ValueError("Database type not supported.")


Base = declarative_base()


class DbReceipt(Base):
    """Receipt model

    Attributes:
        id (int): Receipt id
        transaction_id (str): Transaction id
        datetime (datetime): Receipt datetime
        location (int): Location id
        total_price (float): Receipt total price
        total_discount (float): Receipt total discount
        pickle (bytes): Receipt pickle
    """
    __tablename__ = "receipts" 

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(255), nullable=False)
    datetime = Column(DateTime)
    location = Column(Integer, ForeignKey("locations.id"))
    total_price = Column(Float)
    total_discount = Column(Float)
    pickle = Column(LargeBinary)


class DbProduct(Base):
    """Product model

    Attributes:
        id (int): Product id
        product_id (str): Product id
        description (str): Product description
        name (str): Product name
        receipt (int): Receipt id
        quantity (int): Product quantity
        unit (str): Product unit
        price (float): Product price
        total_price (float): Product total price
        potential_products (bytes): Potential products
        product_not_found (bool): Product not found
    """
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    product_id = Column(String(255))
    description = Column(String(255))
    name = Column(String(255))
    receipt = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    quantity = Column(Integer)
    unit = Column(String(255))
    price = Column(Float)
    total_price = Column(Float)
    potential_products = Column(LargeBinary)
    product_not_found = Column(Boolean)
    

class DbDiscount(Base):
    """Discount model

    Attributes:
        id (int): Discount id
        receipt (int): Receipt id
        type (str): Discount type
        description (str): Discount description
        amount (float): Discount amount
    """
    __tablename__ = "discounts"
    id = Column(Integer, primary_key=True)
    receipt = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    type = Column(String(255))
    description = Column(String(255))
    amount = Column(Float)


class DbCategory(Base):
    """Category model

    Attributes:
        id (int): Category id
        name (str): Category name
        slug (str): Category slug
        english (str): Category english name
        taxonomy_id (str): Category taxonomy id
    """
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    slug = Column(String(255), nullable=False, unique=True)
    english = Column(String(255), nullable=False, unique=False)
    taxonomy_id = Column(String(255), nullable=False, unique=True)


class DbLocation(Base):
    """Location model
    
    Attributes:
        id (int): Location id
        name (str): Location name
        address (str): Location address
        house_number (str): Location house number
        city (str): Location city
        postal_code (str): Location postal code
    """
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(255))
    house_number = Column(String(255))
    city = Column(String(255))
    postal_code = Column(String(255))


class DbCategoryProduct(Base):
    """CategoryProduct model

    Attributes:
        id (int): CategoryProduct id
        taxonomy_id (str): Category taxonomy id
        product_id (str): Product id
    """
    __tablename__ = "categories_products"
    id = Column(Integer, primary_key=True)
    taxonomy_id = Column(String(255), ForeignKey("categories.taxonomy_id"))
    product_id = Column(String(255), ForeignKey("products.product_id"))


class DbCategoryHierarchy(Base):
    """CategoryHierarchy model
    
    Attributes:
        id (int): CategoryHierarchy id
        parent (str): Parent category taxonomy id
        child (str): Child category taxonomy id
    """
    __tablename__ = "categories_hierarchy"
    id = Column(Integer, primary_key=True)
    parent = Column(Integer, ForeignKey("categories.taxonomy_id"))
    child = Column(Integer, ForeignKey("categories.taxonomy_id"))


Base.metadata.create_all(engine)
