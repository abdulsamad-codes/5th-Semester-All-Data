class CartItem:
    def __init__(self, item_id: int, name: str, price: float, quantity: int):
        self.item_id = item_id
        self.name = name
        self.price = price
        self.quantity = quantity

    def get_total(self) -> float:
        """Returns the total cost for this item (price multiplied by quantity)."""
        return self.price * self.quantity

    def to_dict(self) -> dict:
        """Returns a dictionary representation of the cart item."""
        return {
            "item_id": self.item_id,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "total": self.get_total()
        }

class DiscountedItem(CartItem):
    def __init__(self, item_id: int, name: str, price: float, quantity: int, discount_percent: float):
        # Inherit from CartItem using super().__init__()
        super().__init__(item_id, name, price, quantity)
        self.discount_percent = discount_percent

    def get_total(self) -> float:
        """Overrides get_total to apply the percentage discount."""
        base_total = super().get_total()
        return base_total * (1 - self.discount_percent / 100)

    def to_dict(self) -> dict:
        """Overrides to_dict to include the discount percentage and updated total."""
        item_dict = super().to_dict()
        # Insert the discount percent into the dictionary
        item_dict["discount_percent"] = self.discount_percent
        # Update the total to reflect the discounted price
        item_dict["total"] = self.get_total()
        return item_dict


import copy

class ShoppingCart:
    def __init__(self):
        # Private list attribute holding CartItem or DiscountedItem objects
        self._items = []

    def add_item(self, item: CartItem):
        """Adds an item or updates the quantity if the item_id already exists."""
        for existing_item in self._items:
            if existing_item.item_id == item.item_id:
                existing_item.quantity += item.quantity
                return
        
        # If it doesn't exist, append the new item
        self._items.append(item)

    def get_cart_summary(self) -> dict:
        """
        Returns a dictionary summary of the cart.
        Ensures State Isolation so external modifications do not affect internal items.
        """
        # copy.deepcopy ensures that nested dictionaries and totals are entirely isolated
        items_list = [copy.deepcopy(item.to_dict()) for item in self._items]
        grand_total = sum(item.get_total() for item in self._items)
        
        return {
            "items": items_list,
            "grand_total": grand_total
        }

def process_checkout(cart: ShoppingCart, user_balance: float) -> tuple[bool, str]:
    """
    Handles checkout processing outside the ShoppingCart to maintain the 
    Single Responsibility Principle (SRP).
    """
    summary = cart.get_cart_summary()
    
    # Rule 1: If cart has no items, return early
    if not summary["items"]:
        return (False, "Cart is empty")
    
    # Rule 2: Calculate grand_total from the cart summary
    grand_total = summary["grand_total"]
    
    # Rule 3: Check for sufficient funds
    if user_balance < grand_total:
        return (False, "Insufficient funds")
    
    # Rule 4: Successful checkout calculation
    remaining_balance = user_balance - grand_total
    return (True, f"Checkout successful. Remaining balance: PKR {remaining_balance:.2f}")


