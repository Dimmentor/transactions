from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class TransactionCreate(BaseModel):
    id: str
    user_id: int
    amount: float
    currency: str
    category: Optional[str] = None
    description: Optional[str] = ""
    timestamp: datetime


class TransactionRead(BaseModel):
    id: str
    user_id: int
    amount: float
    currency: Optional[str] = "RUB"
    category_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
