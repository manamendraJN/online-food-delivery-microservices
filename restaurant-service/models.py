from pydantic import BaseModel
from typing import Optional


class Restaurant(BaseModel):
    id: int
    name: str
    cuisine: str
    city: str


class RestaurantCreate(BaseModel):
    name: str
    cuisine: str
    city: str


class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    cuisine: Optional[str] = None
    city: Optional[str] = None
