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
)
from config import Config


config = Config()


if config.get("database")["type"] == "sqlite":
    engine = create_engine(f"sqlite:///{config.get('database')['name']}.db")
elif config.get("database")["type"] == "mysql":
    engine = create_engine(
        f"mysql+pymysql://{config.get('database')['username']}:{config.get('database')['password']}@{config.get('database')['host']}/{config.get('database')['name']}"
    )
elif config.get("database")["type"] == "postgresql" or config.get("database")["type"] == "postgres":
    engine = create_engine(
        f"postgresql://{config.get('database')['username']}:{config.get('database')['password']}@{config.get('database')['host']}/{config.get('database')['name']}"
    )
else:
    raise ValueError("Database type not supported.")


Base = declarative_base()


class DbReceipt(Base):
    __tablename__ = "receipts" 

    id = Column(Integer, primary_key=True)
    transaction_id = Column(String(255), nullable=False)
    datetime = Column(DateTime)
    location = Column(Integer, ForeignKey("locations.id"))
    total_price = Column(Float)
    total_discount = Column(Float)
    pickle = Column(LargeBinary)


class DbProduct(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    name = Column(String(255))
    receipt = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    quantity = Column(Integer)
    unit = Column(String(255))
    price = Column(Float)
    total_price = Column(Float)
    categories = Column(String(255))
    category = Column(Integer, ForeignKey("categories.id"))
    

class DbDiscount(Base):
    __tablename__ = "discounts"
    id = Column(Integer, primary_key=True)
    receipt = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    type = Column(String(255))
    description = Column(String(255))
    amount = Column(Float)


class DbCategory(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)


class DbLocation(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    address = Column(String(255))
    house_number = Column(String(255))
    city = Column(String(255))
    postal_code = Column(String(255))


class DbCategoryItem(Base):
    __tablename__ = "categories_items"
    id = Column(Integer, primary_key=True)
    tag = Column(Integer, ForeignKey("categories.id"))
    item = Column(Integer, ForeignKey("products.id"))


class DbCategoryHierarchy(Base):
    __tablename__ = "categories_hierarchy"
    id = Column(Integer, primary_key=True)
    parent = Column(Integer, ForeignKey("categories.id"))
    child = Column(Integer, ForeignKey("categories.id"))


Base.metadata.create_all(engine)
