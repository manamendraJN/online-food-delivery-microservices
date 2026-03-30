from pydantic import BaseModel
from typing import Optional


class Payment(BaseModel):
    id: int
    order_id: int
    amount: float
    method: str
    status: str


class PaymentCreate(BaseModel):
    order_id: int
    amount: float
    method: str
    status: str


class PaymentUpdate(BaseModel):
    order_id: Optional[int] = None
    amount: Optional[float] = None
    method: Optional[str] = None
    status: Optional[str] = None
