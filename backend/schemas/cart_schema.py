<<<<<<< HEAD
from decimal import Decimal

from pydantic import BaseModel, Field
from typing import List
from uuid import UUID, uuid4

class OrderItem(BaseModel):
    menu_item_id: UUID = Field(default_factory=uuid4)
    quantity: int
    price_at_time: Decimal
=======
from pydantic import BaseModel
from typing import List
from uuid import UUID

class OrderItem(BaseModel):
    menu_item_id: UUID
    quantity: int
    price_at_time: float
>>>>>>> order_servicev2

class Cart(BaseModel):
    customer_id: str
    items: List[OrderItem] = []