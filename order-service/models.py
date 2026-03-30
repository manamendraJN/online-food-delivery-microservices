from pydantic import BaseModel
from typing import Optional


class Order(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    total_amount: float
    status: str


class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    total_amount: float
    status: str


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    restaurant_id: Optional[int] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
