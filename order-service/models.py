from pydantic import BaseModel
from typing import Optional, List


class Order(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    total_amount: float
    status: str
    delivery_address: Optional[str] = None
    contact_phone: Optional[str] = None
    items: Optional[List[str]] = None
    special_instructions: Optional[str] = None
    payment_method: Optional[str] = None


class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    total_amount: float
    status: str = "PLACED"
    delivery_address: Optional[str] = None
    contact_phone: Optional[str] = None
    items: Optional[List[str]] = None
    special_instructions: Optional[str] = None
    payment_method: Optional[str] = None


class OrderUpdate(BaseModel):
    user_id: Optional[int] = None
    restaurant_id: Optional[int] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    delivery_address: Optional[str] = None
    contact_phone: Optional[str] = None
    items: Optional[List[str]] = None
    special_instructions: Optional[str] = None
    payment_method: Optional[str] = None
