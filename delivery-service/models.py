from pydantic import BaseModel
from typing import Optional


class Delivery(BaseModel):
    id: int
    order_id: int
    rider_name: str
    current_location: str
    status: str


class DeliveryCreate(BaseModel):
    order_id: int
    rider_name: str
    current_location: str
    status: str


class DeliveryUpdate(BaseModel):
    order_id: Optional[int] = None
    rider_name: Optional[str] = None
    current_location: Optional[str] = None
    status: Optional[str] = None
