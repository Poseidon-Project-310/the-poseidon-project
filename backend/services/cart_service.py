from fastapi import HTTPException
from backend.schemas.cart_schema import Cart
from backend.schemas.order_schema import OrderItem, OrderItemCreate, OrderItemUpdate
from backend.repositories.user_repository import UserRepository

class CartService:
    def __init__(self, user_repository=None):
        self.user_repo = user_repository or UserRepository()

    def get_cart(self, customer_id: str) -> Cart:
        """Finds the user and returns their embedded cart."""
        users = self.user_repo.load_all()
        user = next((u for u in users if u.get("id") == customer_id), None)
        
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # If the user exists but hasn't added anything yet, they might not have a 'cart' key
        cart_data = user.get("cart", {})
        return Cart(**cart_data)

    def add_item(self, customer_id: str, item: OrderItemCreate) -> Cart:
        """Adds an item to the user's cart."""
        cart = self.get_cart(customer_id)
        
        existing_item = next((i for i in cart.items if i.menu_item_id == item.menu_item_id), None)
        
        if existing_item:
            existing_item.quantity += item.quantity
        else:
            cart.items.append(item)
                    
        self._save_cart_to_user(customer_id, cart)
        return cart
    
    def remove_item(self, customer_id: str, menu_item_id: int) -> Cart:
        """Removes an item from the user's cart."""
        cart = self.get_cart(customer_id)
        cart.items = [item for item in cart.items if item.menu_item_id != menu_item_id]

        self._save_cart_to_user(customer_id, cart)
        return cart
    
    def update_item_quantity(self, customer_id: str, menu_item_id: int, quantity: int) -> Cart:
        """Updates the quantity of an item in the user's cart."""
        if quantity <= 0:
            return self.remove_item(customer_id, menu_item_id)
        
        cart = self.get_cart(customer_id)
        item = next((i for i in cart.items if i.menu_item_id == menu_item_id), None)
        
        if not item:
            raise HTTPException(status_code=404, detail="Item not found in cart")
        
        item.quantity = quantity
        
        self._save_cart_to_user(customer_id, cart)
        return cart

    def clear_cart(self, customer_id: str) -> Cart:
        """Resets the user's cart to empty."""
        cart = Cart(items=[])
        self._save_cart_to_user(customer_id, cart)
        return cart
        
    def _save_cart_to_user(self, customer_id: str, updated_cart: Cart):
        """Helper to attach the cart back to the user and save."""
        users = self.user_repo.load_all()
        user_idx = next((i for i, u in enumerate(users) if u.get("id") == customer_id), None)
        
        if user_idx is None:
            raise HTTPException(status_code=404, detail="User not found")
            
        # Overwrite the user's cart with the new dictionary
        users[user_idx]["cart"] = updated_cart.model_dump()
        
        # Save all users back to users.json
        self.user_repo.save_all(users)