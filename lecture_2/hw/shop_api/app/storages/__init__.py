from .cart_storage import CartStorage
from .item_storage import ItemStorage

cart_storage = CartStorage()
item_storage = ItemStorage()

__all__ = [
    "cart_storage",
    "item_storage",
]
