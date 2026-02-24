# Customer Model class

from readline import backend

from backend.models.restaurant.menu_item_model import MenuItem
from backend.models.user.user_model import User

class Customer(User):
    # Inherit info from user
    def __init__(self, email, phone, address, city, postal_code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.postal_code = postal_code
        self.cart = {}  # Initialize an empty cart for the customer
        
    def update_info(self, email: str = None, phone: str = None, address: str = None, city: str = None, postal_code: str = None) -> None:
        # Update customer's personal information
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        if address is not None:
            self.address = address
        if city is not None:
            self.city = city
        if postal_code is not None:
            self.postal_code = postal_code
        
    def add_to_cart(self, item: "MenuItem", quantity: int) -> None:
        # Adds a menu item to the customer's cart with the specified quantity
        # TODO: Replace with actual cart implementation once Cart class is created
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        if not hasattr(self, "cart"):
            self.cart = {}
        if item.id in self.cart:
            self.cart[item.id] += quantity
        else:
            self.cart[item.id] = quantity

    def place_order(self) -> "Order":
        # Places an order based on the items in the customer's cart
        # TODO: Replace with actual order implementation once Order class is created
        pass

    def submit_review(self, order: "Order", rating: int, comment: str) -> "Review":
        # Submits a review for a completed order
        # TODO: Replace with actual review implementation once Review class is created
        pass