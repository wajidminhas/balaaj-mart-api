from datetime import datetime
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    products: List["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    stock: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"onupdate": datetime.utcnow})
    category: Optional[Category] = Relationship(back_populates="products")
    images: List["ProductImage"] = Relationship(back_populates="product")
    attributes: List["ProductAttribute"] = Relationship(back_populates="product")
    reviews: List["ProductReview"] = Relationship(back_populates="product")
    tags: List["ProductTag"] = Relationship(back_populates="product")
    discounts: List["ProductDiscount"] = Relationship(back_populates="product")

class ProductImage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    image_url: str
    product: Optional[Product] = Relationship(back_populates="images")

class ProductAttribute(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    attribute_name: str
    attribute_value: str
    product: Optional[Product] = Relationship(back_populates="attributes")

class ProductReview(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    user_id: int
    rating: int = Field(gt=0, lt=6)
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    product: Optional[Product] = Relationship(back_populates="reviews")

class ProductTag(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    tag_name: str
    product: Optional[Product] = Relationship(back_populates="tags")

class ProductDiscount(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    discount_value: float
    discount_type: str = Field(regex="^(percentage|fixed)$")
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    product: Optional[Product] = Relationship(back_populates="discounts")
