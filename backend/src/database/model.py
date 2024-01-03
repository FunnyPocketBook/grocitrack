from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    ForeignKey,
    Column,
    Integer,
    Float,
    String,
    DateTime,
    Boolean,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
import datetime

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
    """

    __tablename__ = "receipts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    transaction_id = Column(String(255), nullable=False)
    datetime = Column(DateTime)
    location = Column(Integer, ForeignKey("locations.id"))
    total_price = Column(Float)
    total_discount = Column(Float)

    def toJSON(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "datetime": self.datetime,
            "location": self.location,
            "total_price": self.total_price,
            "total_discount": self.total_discount,
        }


class DbAHProducts(Base):
    """AHProducts model. Mirrors the products that are available in the AH API.

    Attributes:
        id (int): Product id
        webshop_id (str): Product webshop id
        hq_id (str): Product hq id
        title (str): Product title
        sales_unit_size (str): Product sales unit size
        images (JSON): Product images
        price_before_bonus (float): Product price before bonus
        order_availability_status (str): Product order availability status
        main_category (str): Product main category
        sub_category (str): Product sub category
        brand (str): Product brand
        shop_type (str): Product shop type
        available_online (bool): Product available online
        is_previously_bought (bool): Product is previously bought
        description_highlights (str): Product description highlights
        nutriscore (str): Product nutriscore
        nix18 (bool): Product nix18
        is_stapel_bonus (bool): Product is stapel bonus
        property_icons (JSON): Product property icons
        extra_descriptions (JSON): Product extra descriptions
        is_bonus (bool): Product is bonus
        description_full (str): Product description full
        is_orderable (bool): Product is orderable
        is_infinite_bonus (bool): Product is infinite bonus
        is_sample (bool): Product is sample
        is_sponsored (bool): Product is sponsored
        discount_labels (JSON): Product discount labels
        unit_price_description (str): Product unit price description
        auction_id (str): Product auction id
        bonus_start_date (datetime): Product bonus start date
        bonus_end_date (datetime): Product bonus end date
        discount_type (str): Product discount type
        segment_type (str): Product segment type
        promotion_type (str): Product promotion type
        bonus_mechanism (str): Product bonus mechanism
        current_price (float): Product current price
        bonus_period_description (str): Product bonus period description
        bonus_segment_id (str): Product bonus segment id
        bonus_segment_description (str): Product bonus segment description
        has_list_price (bool): Product has list price
        is_bonus_price (bool): Product is bonus price
        product_count (int): Product count
        multiple_item_promotion (bool): Product multiple item promotion
        stickers (JSON): Product stickers
        order_availability_description (str): Product order availability description
        date_added (datetime): Product date added
    """

    __tablename__ = "ah_products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    webshop_id = Column(String(255))
    hq_id = Column(String(255))
    title = Column(String(255))
    sales_unit_size = Column(String(255))
    images = Column(JSONB)
    price_before_bonus = Column(Float)
    order_availability_status = Column(String(255))
    main_category = Column(String(255))
    sub_category = Column(String(255))
    brand = Column(String(255))
    shop_type = Column(String(255))
    available_online = Column(Boolean)
    is_previously_bought = Column(Boolean)
    description_highlights = Column(Text)
    nutriscore = Column(String(1))
    nix18 = Column(Boolean)
    is_stapel_bonus = Column(Boolean)
    property_icons = Column(JSONB)
    extra_descriptions = Column(JSONB)
    is_bonus = Column(Boolean)
    description_full = Column(Text)
    is_orderable = Column(Boolean)
    is_infinite_bonus = Column(Boolean)
    is_sample = Column(Boolean)
    is_sponsored = Column(Boolean)
    discount_labels = Column(JSONB)
    unit_price_description = Column(String(255))
    auction_id = Column(String(255))
    bonus_start_date = Column(DateTime)
    bonus_end_date = Column(DateTime)
    discount_type = Column(String(255))
    segment_type = Column(String(255))
    promotion_type = Column(String(255))
    bonus_mechanism = Column(String(255))
    current_price = Column(Float)
    bonus_period_description = Column(String(255))
    bonus_segment_id = Column(String(255))
    bonus_segment_description = Column(String(255))
    has_list_price = Column(Boolean)
    is_bonus_price = Column(Boolean)
    product_count = Column(Integer)
    multiple_item_promotion = Column(Boolean)
    stickers = Column(JSONB)
    order_availability_description = Column(String(255))
    date_added = Column(DateTime)
    # date_added = Column(DateTime, default=lambda: datetime.datetime.now(datetime.UTC))


class DbPreviousProducts(Base):
    """PreviousProducts model.

    Attributes:
        id (int): Product id
        webshop_id (str): Product webshop id
        hq_id (str): Product hq id
        title (str): Product title
        sales_unit_size (str): Product sales unit size
        images (JSON): Product images
        price_before_bonus (float): Product price before bonus
        order_availability_status (str): Product order availability status
        main_category (str): Product main category
        sub_category (str): Product sub category
        brand (str): Product brand
        shop_type (str): Product shop type
        available_online (bool): Product available online
        is_previously_bought (bool): Product is previously bought
        description_highlights (str): Product description highlights
        nutriscore (str): Product nutriscore
        nix18 (bool): Product nix18
        is_stapel_bonus (bool): Product is stapel bonus
        property_icons (JSON): Product property icons
        extra_descriptions (JSON): Product extra descriptions
        is_bonus (bool): Product is bonus
        description_full (str): Product description full
        is_orderable (bool): Product is orderable
        is_infinite_bonus (bool): Product is infinite bonus
        is_sample (bool): Product is sample
        is_sponsored (bool): Product is sponsored
        discount_labels (JSON): Product discount labels
        unit_price_description (str): Product unit price description
        auction_id (str): Product auction id
        bonus_start_date (datetime): Product bonus start date
        bonus_end_date (datetime): Product bonus end date
        discount_type (str): Product discount type
        segment_type (str): Product segment type
        promotion_type (str): Product promotion type
        bonus_mechanism (str): Product bonus mechanism
        current_price (float): Product current price
        bonus_period_description (str): Product bonus period description
        bonus_segment_id (str): Product bonus segment id
        bonus_segment_description (str): Product bonus segment description
        has_list_price (bool): Product has list price
        is_bonus_price (bool): Product is bonus price
        product_count (int): Product count
        multiple_item_promotion (bool): Product multiple item promotion
        stickers (JSON): Product stickers
        order_availability_description (str): Product order availability description
    """

    __tablename__ = "previous_products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    webshop_id = Column(String(255))
    hq_id = Column(String(255))
    title = Column(String(255))
    sales_unit_size = Column(String(255))
    images = Column(JSONB)
    price_before_bonus = Column(Float)
    order_availability_status = Column(String(255))
    main_category = Column(String(255))
    sub_category = Column(String(255))
    brand = Column(String(255))
    shop_type = Column(String(255))
    available_online = Column(Boolean)
    is_previously_bought = Column(Boolean)
    description_highlights = Column(Text)
    nutriscore = Column(String(1))
    nix18 = Column(Boolean)
    is_stapel_bonus = Column(Boolean)
    property_icons = Column(JSONB)
    extra_descriptions = Column(JSONB)
    is_bonus = Column(Boolean)
    description_full = Column(Text)
    is_orderable = Column(Boolean)
    is_infinite_bonus = Column(Boolean)
    is_sample = Column(Boolean)
    is_sponsored = Column(Boolean)
    discount_labels = Column(JSONB)
    unit_price_description = Column(String(255))
    auction_id = Column(String(255))
    bonus_start_date = Column(DateTime)
    bonus_end_date = Column(DateTime)
    discount_type = Column(String(255))
    segment_type = Column(String(255))
    promotion_type = Column(String(255))
    bonus_mechanism = Column(String(255))
    current_price = Column(Float)
    bonus_period_description = Column(String(255))
    bonus_segment_id = Column(String(255))
    bonus_segment_description = Column(String(255))
    has_list_price = Column(Boolean)
    is_bonus_price = Column(Boolean)
    product_count = Column(Integer)
    multiple_item_promotion = Column(Boolean)
    stickers = Column(JSONB)
    order_availability_description = Column(String(255))


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
        potential_products (JSON): Potential products
        product_not_found (bool): Product not found
    """

    __tablename__ = "products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(String(255))
    description = Column(String(255))
    name = Column(String(255))
    receipt = Column(Integer, ForeignKey("receipts.id"), nullable=False)
    quantity = Column(Integer)
    unit = Column(String(255))
    price = Column(Float)
    total_price = Column(Float)
    product_not_found = Column(Boolean)
    potential_products = Column(JSONB)


class DbPotentialProduct(Base):
    """PotentialProduct model

    Attributes:
        id (int): PotentialProduct id
        product (int): Product id
        potential_ah_product (int): Potential AHProduct id
        potential_previous_product (int): Potential PreviousProduct id"""

    __tablename__ = "potential_products"
    id = Column(Integer, primary_key=True, autoincrement=True)
    product = Column(Integer, ForeignKey("products.id"), nullable=False)
    potential_ah_product = Column(Integer, ForeignKey("ah_products.id"), nullable=True)
    potential_previous_product = Column(
        Integer, ForeignKey("previous_products.id"), nullable=True
    )


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
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    id = Column(Integer, primary_key=True, autoincrement=True)
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    taxonomy_id = Column(String(255), ForeignKey("categories.taxonomy_id"))
    product_id = Column(String(255))


class DbCategoryHierarchy(Base):
    """CategoryHierarchy model

    Attributes:
        id (int): CategoryHierarchy id
        parent (str): Parent category taxonomy id
        child (str): Child category taxonomy id
    """

    __tablename__ = "categories_hierarchy"
    id = Column(Integer, primary_key=True, autoincrement=True)
    parent = Column(String(255), ForeignKey("categories.taxonomy_id"))
    child = Column(String(255), ForeignKey("categories.taxonomy_id"))
