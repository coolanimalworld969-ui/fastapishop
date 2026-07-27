from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapishop.database import Base
from enum import Enum
from decimal import Decimal

from fastapishop.models import ProductOrm, UsersOrm


class OrderStatus(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class OrderOrm(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.PENDING)

    created_at: Mapped[datetime] = mapped_column(
     server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
     server_default=func.now(),
     onupdate=func.now()
    )

    order_items: Mapped[list["OrderItemOrm"]] = relationship("OrderItemOrm", back_populates="order", cascade="all, delete-orphan")

    user: Mapped["UsersOrm"] = relationship("UsersOrm", back_populates="orders")

class OrderItemOrm(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    # Связь с продуктом
    product: Mapped["ProductOrm"] = relationship("ProductOrm")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    # ----
    quantity: Mapped[int]
    price: Mapped[Decimal]

    order: Mapped["OrderOrm"] = relationship("OrderOrm", back_populates="order_items")