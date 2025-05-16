from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.database import Base


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[str] = mapped_column(String, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.id'), nullable=False)
    timestamp: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped["User"] = relationship("User", back_populates="transactions")
    category: Mapped["Category"] = relationship("Category", back_populates="transactions")