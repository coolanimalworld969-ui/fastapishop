from datetime import datetime

from sqlalchemy import ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from models import CategoryOrm


class ProductOrm(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    name: Mapped[str]
    price: Mapped[int] = mapped_column(Numeric(10,2))
    stock: Mapped[int] = mapped_column(default=0)

    category: Mapped["CategoryOrm"] = relationship("CategoryOrm", back_populates="products")

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )