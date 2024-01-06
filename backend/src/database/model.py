from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    Integer,
    Float,
    String,
    DateTime,
    Boolean,
)
from sqlalchemy.dialects.postgresql import JSONB
import datetime as dt

class Base(DeclarativeBase):
    pass


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

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    transaction_id: Mapped[str] = mapped_column(String(255), nullable=False)
    datetime: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True))
    location: Mapped[int] = mapped_column(Integer, ForeignKey("locations.id"))
    total_price: Mapped[float] = mapped_column(Float)
    total_discount: Mapped[float] = mapped_column(Float)

    products: Mapped[list["DbProduct"]] = relationship(
        "DbProduct", back_populates="receipt_relation"
    )
    discounts: Mapped[list["DbDiscount"]] = relationship(
        "DbDiscount", back_populates="receipt_relation"
    )
    location_relation: Mapped["DbLocation"] = relationship(
        "DbLocation", back_populates="receipt_relation"
    )

    def toJSON(self):
        return {
            "id": self.id,
            "transaction_id": self.transaction_id,
            "datetime": self.datetime,
            "location": self.location,
            "total_price": self.total_price,
            "total_discount": self.total_discount,
        }

class DbAHProduct(Base):
    """AHProduct model. Mirrors the products that are available in the AH API.

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
        nutriscore (str): Product nutriscore
        nix18 (bool): Product nix18
        is_stapel_bonus (bool): Product is stapel bonus
        property_icons (JSON): Product property icons
        is_bonus (bool): Product is bonus
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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    webshop_id: Mapped[str] = mapped_column(String(255), nullable=True)
    hq_id: Mapped[str] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    sales_unit_size: Mapped[str] = mapped_column(String(255), nullable=True)
    images: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    price_before_bonus: Mapped[float] = mapped_column(Float, nullable=True)
    order_availability_status: Mapped[str] = mapped_column(String(255), nullable=True)
    main_category: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_category: Mapped[str] = mapped_column(String(255), nullable=True)
    brand: Mapped[str] = mapped_column(String(255), nullable=True)
    shop_type: Mapped[str] = mapped_column(String(255), nullable=True)
    available_online: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_previously_bought: Mapped[bool] = mapped_column(Boolean, nullable=True)
    nutriscore: Mapped[str] = mapped_column(String(1), nullable=True)
    nix18: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_stapel_bonus: Mapped[bool] = mapped_column(Boolean, nullable=True)
    property_icons: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    is_bonus: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_orderable: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_infinite_bonus: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_sample: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_sponsored: Mapped[bool] = mapped_column(Boolean, nullable=True)
    discount_labels: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    unit_price_description: Mapped[str] = mapped_column(String(255), nullable=True)
    auction_id: Mapped[str] = mapped_column(String(255), nullable=True)
    bonus_start_date: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    bonus_end_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    discount_type: Mapped[str] = mapped_column(String(255), nullable=True)
    segment_type: Mapped[str] = mapped_column(String(255), nullable=True)
    promotion_type: Mapped[str] = mapped_column(String(255), nullable=True)
    bonus_mechanism: Mapped[str] = mapped_column(String(255), nullable=True)
    current_price: Mapped[float] = mapped_column(Float, nullable=True)
    bonus_period_description: Mapped[str] = mapped_column(String(255), nullable=True)
    bonus_segment_id: Mapped[str] = mapped_column(String(255), nullable=True)
    bonus_segment_description: Mapped[str] = mapped_column(String(255), nullable=True)
    has_list_price: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_bonus_price: Mapped[bool] = mapped_column(Boolean, nullable=True)
    product_count: Mapped[int] = mapped_column(Integer, nullable=True)
    multiple_item_promotion: Mapped[bool] = mapped_column(Boolean, nullable=True)
    stickers: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    order_availability_description: Mapped[str] = mapped_column(String(255), nullable=True)
    date_added: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    potential_products: Mapped[list["DbPotentialProduct"]] = relationship(
        "DbPotentialProduct", back_populates="ah_product_relation"
    )


class DbPreviousProduct(Base):
    """PreviousProduct model.

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
        nutriscore (str): Product nutriscore
        nix18 (bool): Product nix18
        is_stapel_bonus (bool): Product is stapel bonus
        property_icons (JSON): Product property icons
        is_bonus (bool): Product is bonus
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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    webshop_id: Mapped[str] = mapped_column(String(255), nullable=True)
    hq_id: Mapped[str] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    sales_unit_size: Mapped[str] = mapped_column(String(255), nullable=True)
    images: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    price_before_bonus: Mapped[float] = mapped_column(Float, nullable=True)
    order_availability_status: Mapped[str] = mapped_column(String(255), nullable=True)
    main_category: Mapped[str] = mapped_column(String(255), nullable=True)
    sub_category: Mapped[str] = mapped_column(String(255), nullable=True)
    brand: Mapped[str] = mapped_column(String(255), nullable=True)
    shop_type: Mapped[str] = mapped_column(String(255), nullable=True)
    available_online: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_previously_bought: Mapped[bool] = mapped_column(Boolean, nullable=True)
    nutriscore: Mapped[str] = mapped_column(String(1), nullable=True)
    nix18: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_stapel_bonus: Mapped[bool] = mapped_column(Boolean, nullable=True)
    property_icons: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    is_bonus: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_orderable: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_infinite_bonus: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_sample: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_sponsored: Mapped[bool] = mapped_column(Boolean, nullable=True)
    discount_labels: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    unit_price_description: Mapped[str] = mapped_column(String(255), nullable=True)
    auction_id: Mapped[str] = mapped_column(String(255), nullable=True)
    bonus_start_date: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    bonus_end_date: Mapped[dt.datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    discount_type: Mapped[str] = mapped_column(String(255), nullable=True)
    segment_type: Mapped[str] = mapped_column(String(255), nullable=True)
    promotion_type: Mapped[str] = mapped_column(String(255), nullable=True)
    bonus_mechanism: Mapped[str] = mapped_column(String(255), nullable=True)
    current_price: Mapped[float] = mapped_column(Float, nullable=True)
    bonus_period_description: Mapped[str] = mapped_column(String(255), nullable=True)
    bonus_segment_id: Mapped[str] = mapped_column(String(255), nullable=True)
    bonus_segment_description: Mapped[str] = mapped_column(String(255), nullable=True)
    has_list_price: Mapped[bool] = mapped_column(Boolean, nullable=True)
    is_bonus_price: Mapped[bool] = mapped_column(Boolean, nullable=True)
    product_count: Mapped[int] = mapped_column(Integer, nullable=True)
    multiple_item_promotion: Mapped[bool] = mapped_column(Boolean, nullable=True)
    stickers: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    order_availability_description: Mapped[str] = mapped_column(String(255), nullable=True)

    potential_products: Mapped[list["DbPotentialProduct"]] = relationship(
        "DbPotentialProduct", back_populates="previous_product_relation"
    )

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
        product_not_found (bool): Product not found
    """

    __tablename__ = "products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product_id: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    receipt: Mapped[int] = mapped_column(Integer, ForeignKey("receipts.id"), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=True)
    unit: Mapped[str] = mapped_column(String(255), nullable=True)
    price: Mapped[float] = mapped_column(Float, nullable=True)
    total_price: Mapped[float] = mapped_column(Float, nullable=True)
    potential_products: Mapped[JSONB] = mapped_column(JSONB, nullable=True)
    product_not_found: Mapped[bool] = mapped_column(Boolean, nullable=True)

    receipt_relation: Mapped[DbReceipt] = relationship(
        "DbReceipt", back_populates="products"
    )
    potential_product_relation: Mapped["DbPotentialProduct"] = relationship(
        "DbPotentialProduct", back_populates="product_relation"
    )


class DbPotentialProduct(Base):
    """PotentialProduct model

    Attributes:
        id (int): PotentialProduct id
        product (int): Product id
        potential_ah_product (int): Potential AHProduct id
        potential_previous_product (int): Potential PreviousProduct id"""

    __tablename__ = "potential_products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    product: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    potential_ah_product: Mapped[int] = mapped_column(Integer, ForeignKey("ah_products.id"), nullable=True)
    potential_previous_product: Mapped[int] = mapped_column(Integer, ForeignKey("previous_products.id"), nullable=True)

    product_relation: Mapped[DbProduct] = relationship(
        "DbProduct", back_populates="potential_product_relation"
    )
    ah_product_relation: Mapped[DbAHProduct] = relationship(
        "DbAHProduct", back_populates="potential_products"
    )
    previous_product_relation: Mapped[DbPreviousProduct] = relationship(
        "DbPreviousProduct", back_populates="potential_products"
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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    receipt: Mapped[int] = mapped_column(Integer, ForeignKey("receipts.id"), nullable=False)
    type: Mapped[str] = mapped_column(String(255), nullable=True)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    amount: Mapped[float] = mapped_column(Float, nullable=True)

    receipt_relation: Mapped[DbReceipt] = relationship(
        "DbReceipt", back_populates="discounts"
    )


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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(String(255), nullable=False)
    english: Mapped[str] = mapped_column(String(255), nullable=False)
    taxonomy_id: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    category_product_relation: Mapped["DbCategoryProduct"] = relationship(
        "DbCategoryProduct", back_populates="category"
    )
    category_hierarchy_parent_relation: Mapped["DbCategoryHierarchy"] = relationship(
        "DbCategoryHierarchy", back_populates="parent_category", foreign_keys="[DbCategoryHierarchy.parent]"
    )
    category_hierarchy_child_relation: Mapped["DbCategoryHierarchy"] = relationship(
        "DbCategoryHierarchy", back_populates="child_category", foreign_keys="[DbCategoryHierarchy.child]"
    )

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255))
    house_number: Mapped[str] = mapped_column(String(255))
    city: Mapped[str] = mapped_column(String(255))
    postal_code: Mapped[str] = mapped_column(String(255))

    receipt_relation: Mapped[DbReceipt] = relationship(
        "DbReceipt", back_populates="location_relation"
    )


class DbCategoryProduct(Base):
    """CategoryProduct model

    Attributes:
        id (int): CategoryProduct id
        taxonomy_id (str): Category taxonomy id
        product_id (str): Product id (webshop id)
    """

    __tablename__ = "categories_products"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    taxonomy_id: Mapped[str] = mapped_column(String(255), ForeignKey("categories.taxonomy_id"))
    product_id: Mapped[str] = mapped_column(String(255))

    category: Mapped[DbCategory] = relationship(
        "DbCategory", back_populates="category_product_relation"
    )


class DbCategoryHierarchy(Base):
    """CategoryHierarchy model

    Attributes:
        id (int): CategoryHierarchy id
        parent (str): Parent category taxonomy id
        child (str): Child category taxonomy id
    """

    __tablename__ = "categories_hierarchy"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    parent: Mapped[str] = mapped_column(String(255), ForeignKey("categories.taxonomy_id"))
    child: Mapped[str] = mapped_column(String(255), ForeignKey("categories.taxonomy_id"))

    parent_category: Mapped[DbCategory] = relationship(
        "DbCategory", back_populates="category_hierarchy_parent_relation", foreign_keys=[parent]
    )
    child_category: Mapped[DbCategory] = relationship(
        "DbCategory", back_populates="category_hierarchy_child_relation", foreign_keys=[child]
    )
