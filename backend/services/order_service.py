import uuid
import random
import string
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException

from backend.schemas.order_schema import Order, OrderCreate, OrderUpdate, OrderStatus, OrderItem
from backend.repositories.order_repo import OrderRepository

class OrderValidate:
    @staticmethod
    def validate_delivery_postal_code(value: str) -> str:
        import re
        if value is None: return None
        regex_pattern = r"^[A-Z][0-9][A-Z]\s?[0-9][A-Z][0-9]$"
        formatted_value = value.strip().upper()
        if not re.match(regex_pattern, formatted_value):
            raise ValueError(f"'{value}' is not a valid Canadian postal code (e.g., V1V 1V1)")
        return formatted_value

    @staticmethod
    def validate_delivery_latitude(value: float) -> float:
        if value is not None and not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @staticmethod
    def validate_delivery_longitude(value: float) -> float:
        if value is not None and not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return value

class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def generate_order_id(self) -> str:
        """Generates 6 random hex chars + 1 random uppercase letter. (to follow ID structure in example data)"""
        unique_hex = uuid.uuid4().hex[:6]
        random_letter = random.choice(string.ascii_uppercase)
        return f"{unique_hex}{random_letter}" 

    def create_order(self, payload: OrderCreate) -> Order:
        items = self.repository.load_all()
        # Validate info first
        try:
            lat = OrderValidate.validate_delivery_latitude(payload.delivery_latitude)
            lon = OrderValidate.validate_delivery_longitude(payload.delivery_longitude)
            pc = OrderValidate.validate_delivery_postal_code(payload.delivery_postal_code)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Generate order ID
        id = self.generate_order_id()
        if any(it.get("id") == id for it in items):  # extremely unlikely, but consistent check
            raise HTTPException(status_code=409, detail="ID collision; retry.")

        new_order_data = {
            "id": id,
            "customer_id": payload.customer_id.strip(),
            "restaurant_id": payload.restaurant_id,
            "status": OrderStatus.UNPAID,
            "order_date": datetime.now().isoformat(),
            "delivery_latitude": lat,
            "delivery_longitude": lon,
            "delivery_postal_code": pc,
            "items": [item.model_dump() for item in payload.items],
            # TODO: Feat7 - Integrate fee calculators for these:
            "cost_breakdown": 0
        }
        # Save order to repo
        orders = self.repository.load_all()
        orders.append(new_order_data)
        self.repository.save_all(orders)
        
        return Order(**new_order_data)

    def update_order(self, order_id: str, payload: OrderUpdate) -> Order:
        orders = self.repository.load_all()
        print(f"\n--- DEBUG: orders looks like: {orders} | order_id looks like: {order_id} ---")
        order_idx = next((i for i, o in enumerate(orders) if o.get("id") == order_id), None)
        
        if order_idx is None:
            raise HTTPException(status_code=404, detail="Order not found")

        current_order = orders[order_idx]

        try:
            if payload.status: current_order["status"] = payload.status
            if payload.delivery_latitude: 
                current_order["delivery_latitude"] = OrderValidate.validate_delivery_latitude(payload.delivery_latitude)
            if payload.delivery_longitude:
                current_order["delivery_longitude"] = OrderValidate.validate_delivery_longitude(payload.delivery_longitude)
            if payload.delivery_postal_code:
                current_order["delivery_postal_code"] = OrderValidate.validate_delivery_postal_code(payload.delivery_postal_code)
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

        self.repository.save_all(orders)
        return Order(**current_order)