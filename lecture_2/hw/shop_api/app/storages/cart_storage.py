from typing import Iterable

from .models import Cart, CartItem, Item


class CartStorage:
    def __init__(self):
        self._data = dict[int, Cart]()
        self._id_generator = self._int_id_generator()

    @staticmethod
    def _int_id_generator() -> Iterable[int]:
        i = 0
        while True:
            yield i
            i += 1

    def add(self) -> Cart:
        _id = next(self._id_generator)  # type: ignore
        cart = Cart(_id)
        self._data[_id] = cart

        return cart

    def delete(self, id: int) -> None:
        if id in self._data:
            del self._data[id]

    def get_one(self, id: int) -> Cart | None:
        return self._data[id] if id in self._data else None

    def get_many(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: float | None = None,
        max_price: float | None = None,
        min_quantity: float | None = None,
        max_quantity: float | None = None,
    ) -> Iterable[Cart]:
        curr = 0

        def is_price_suitable(cart):
            if min_price is None and max_price is None:
                return True
            elif min_price is None:
                return cart.price <= max_price
            elif max_price is None:
                return cart.price >= min_price
            else:
                return min_price <= cart.price <= max_price

        def is_quantity_suitable(cart):
            if min_quantity is None and max_quantity is None:
                return True
            elif min_quantity is None:
                return cart.quantity <= max_quantity
            elif max_quantity is None:
                return cart.quantity >= min_quantity
            else:
                return min_quantity <= cart.quantity <= max_quantity

        for cart in self._data.values():
            if (
                offset <= curr < offset + limit
                and is_price_suitable(cart)
                and is_quantity_suitable(cart)
            ):
                yield cart

            curr += 1

    def add_item_to_cart(self, cart_id: int, item: Item) -> CartItem:
        cart = self._data[cart_id]

        if item.id in cart.items:
            cart.items[item.id].quantity += 1
        else:
            cart.items[item.id] = CartItem(id=item.id, info=item.info, quantity=1)

        return cart.items[item.id]
