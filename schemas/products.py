from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from decimal import Decimal
from .categories import CategoryResponse

class ProductCreate(BaseModel):
    category_id: int = Field(gt=0)
    name: str
    price: Decimal
    stock: int = Field(ge=0)

class ProductResponse(BaseModel):
    id: int
    category_id: int
    name: str
    price: Decimal
    stock: int
    category: CategoryResponse
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductOrderResponse(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes=True
    )

class ProductUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = None
    price: Decimal | None = None
    stock: int | None = None