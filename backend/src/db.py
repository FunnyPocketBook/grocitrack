from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    ForeignKey,
    create_engine,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    Table,
)
from config import Config

config = Config()


if config.get("database")["type"] == "sqlite":
    engine = create_engine("sqlite:///" + config.get("database")["name"])
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


class DbProduct(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    receipt = Column(Integer, ForeignKey("receipts.id"))
    quantity = Column(Integer)
    unit = Column(String)
    price = Column(Float)
    total_price = Column(Float)
    category = Column(Integer, ForeignKey("categories.id"))
    

class DbDiscount(Base):
    __tablename__ = "discounts"
    id = Column(Integer, primary_key=True)
    receipt = Column(Integer, ForeignKey("receipts.id"))
    type = Column(String)
    description = Column(String)
    amount = Column(Float)


class DbCategory(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class DbLocation(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    house_number = Column(String)
    city = Column(String)
    postal_code = Column(String)


class DbTag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class TagItem(Base):
    __tablename__ = "tags_items"
    id = Column(Integer, primary_key=True)
    tag = Column(Integer, ForeignKey("tags.id"))
    item = Column(Integer, ForeignKey("products.id"))


Base.metadata.create_all(engine)
