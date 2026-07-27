from sqlalchemy.orm import Mapped, mapped_column, relationship
from fastapishop.database import Base
from datetime import datetime
from sqlalchemy import DateTime, func

class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    age: Mapped[int]
    email: Mapped[str]
    hashed_password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    orders: Mapped[list["OrderOrm"]] = relationship("OrderOrm", back_populates="user")