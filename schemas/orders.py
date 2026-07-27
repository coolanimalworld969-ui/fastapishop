from pydantic import BaseModel, ConfigDict, Field
from fastapishop.models import OrderStatus
from decimal import Decimal

from fastapishop.schemas import ProductOrderResponse, ProductResponse


class OrderResponse(BaseModel):
    id: int
    status: OrderStatus
    order_items: list["OrderItemResponse"]

    model_config = ConfigDict(
        from_attributes=True
    )

class OrderCreate(BaseModel):
    order_items: list["OrderItemCreate"]


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)

class OrderItemResponse(BaseModel):
    price: Decimal
    quantity: int = Field(gt=0)
    product: ProductOrderResponse

    model_config = ConfigDict(
        from_attributes=True
    )