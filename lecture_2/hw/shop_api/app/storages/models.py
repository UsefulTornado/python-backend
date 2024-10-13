from dataclasses import dataclass, field


@dataclass(slots=True)
class ItemInfo:
    name: str
    price: float
    deleted: bool = False


@dataclass(slots=True)
class PatchItemInfo:
    name: str | None = None
    price: float | None = None
    deleted: bool | None = None


@dataclass(slots=True)
class Item:
    id: int
    info: ItemInfo


@dataclass(slots=True)
class CartItem(Item):
    quantity: int = 0


@dataclass(slots=True)
class Cart:
    id: int
    items: dict[int, CartItem] = field(default_factory=dict)

    @property
    def price(self):
        return sum(
            item.info.price for item in self.items.values() if not item.info.deleted
        )

    @property
    def quantity(self):
        return sum(item.quantity for item in self.items.values())
