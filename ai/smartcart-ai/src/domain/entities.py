from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field

class Product(BaseModel):
    product_id: str
    name: str
    category: str
    description: str
    price: float

class CartItem(BaseModel):
    product_id: str
    quantity: int = 1

class Cart(BaseModel):
    user_id: str
    items: List[CartItem] = []

    @property
    def total_items(self) -> int:
        return sum(item.quantity for item in self.items)

class Order(BaseModel):
    order_id: str
    user_id: str
    product_ids: List[str]
    timestamp: datetime

class User(BaseModel):
    user_id: str
    name: str = "Guest"
    email: Optional[str] = None
