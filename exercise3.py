"""Exercise 3: Enforce a business rule.

Extend your Cart so invalid operations are rejected by the CART.

  ValueError        when qty < 1
  OutOfStockError   when the item's "available" field is False
  KeyError          when removing an item that is not in the cart

Then demonstrate each one with try/except.
"""

from exercise1 import load_menu


class OutOfStockError(Exception):
    """Raised when a customer tries to order an item that is unavailable."""
    pass


class Cart:
    def __init__(self) -> None:
        self.lines: list[dict] = []

    def add_item(self, item: dict, qty: int = 1) -> None:
        if qty < 1:
            raise ValueError(qty)
        if not item["available"]:
            raise OutOfStockError(item["name"])
        
        for existing in self.lines:
            if existing["item_id"] == item["id"]:
                existing["qty"] += qty
                return
        self.lines.append(
            {
                "item_id": item["id"],
                "name": item["name"],
                "price": item["price"],
                "qty": qty
            })
        return

    def remove_item(self, item_id: int) -> None:
        for existing in self.lines:
            if existing["item_id"] == item_id:
                self.lines.remove(existing)
                return
        raise KeyError(item_id)

    def total(self) -> float:
        return round(sum(line["price"] * line["qty"] for line in self.lines), 2)

    def __repr__(self) -> str:
        return f"<Cart {len(self.lines)} items, ${self.total():.2f}>"


if __name__ == "__main__":
    menu = load_menu()
    gyoza = menu[1]           # available
    miso = menu[3]            # NOT available

    cart = Cart()

    # TODO: demonstrate each rejection with try/except and a readable message.
    try:
        cart.add_item(gyoza, 0)
    except ValueError as e:
        print(f"Rejected: Quantity cannot be {e}")
        
    try:
        cart.add_item(miso, 1)
    except OutOfStockError as e:
        print(f"Rejected: {e} is not in stock")
        
    try:
        cart.remove_item(1)
    except KeyError as e:
        print(f"Rejected: No items with id of {e} in cart")

