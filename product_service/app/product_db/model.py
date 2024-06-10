from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime, timezone

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float
    category: Optional[str] = None
    stock: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=datetime.now(timezone.utc), sa_column_kwargs={"onupdate": datetime.now(timezone.utc)})
