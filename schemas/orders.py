from pydantic import BaseModel, ConfigDict, Field
from fastapishop.models import OrderStatus

class OrderResponse(BaseModel):
    id: int
    status: OrderStatus

    model_config = ConfigDict(
        from_attributes=True
    )

class OrderCreate(BaseModel):
    order_items: list["OrderItemCreate"]

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)