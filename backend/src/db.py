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

config = {}

if config["database"]["type"] == "sqlite":
    engine = create_engine("sqlite:///" + config["database"]["path"])
elif config["database"]["type"] == "mysql":
    engine = create_engine(
        f"mysql+pymysql://{config['database']['username']}:{config['database']['password']}@{config['database']['host']}/{config['database']['database']}"
    )
elif config["database"]["type"] == "postgresql" or config["database"]["type"] == "postgres":
    engine = create_engine(
        f"postgresql://{config['database']['username']}:{config['database']['password']}@{config['database']['host']}/{config['database']['database']}"
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


# Many-to-many tags and items
tags_items = Table(
    "tags_products",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tags.id")),
    Column("product_id", Integer, ForeignKey("products.id")),
)

Base.metadata.create_all(engine)

# filename = 'mymodel.png'
# render_er(Base.metadata, filename)
# imgplot = plt.imshow(mpimg.imread(filename))
# plt.show()
