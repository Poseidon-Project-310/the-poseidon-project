from typing import List
from pydantic import BaseModel
from backend.schemas.order_schema import OrderItem

class Cart(BaseModel):
    items: List[OrderItem] = []