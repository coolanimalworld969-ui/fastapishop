from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class CategoryOrm(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    products: Mapped[list["ProductOrm"]] = relationship("ProductOrm", back_populates="category")

