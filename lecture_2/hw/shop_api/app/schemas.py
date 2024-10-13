from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from lecture_2.hw.shop_api.app.storages.models import (
    Cart,
    CartItem,
    Item,
    ItemInfo,
    PatchItemInfo,
)


class ItemResponse(BaseModel):
    id: int
    name: str
    price: float

    @staticmethod
    def from_entity(entity: Item) -> ItemResponse:
        return ItemResponse(
            id=entity.id,
            name=entity.info.name,
            price=entity.info.price,
        )


class ItemRequest(BaseModel):
    name: str
    price: float

    def as_item_info(self) -> ItemInfo:
        return ItemInfo(name=self.name, price=self.price)


class PatchItemRequest(BaseModel):
    name: str | None = None
    price: float | None = None

    model_config = ConfigDict(extra="forbid")

    def as_patch_item_info(self) -> PatchItemInfo:
        return PatchItemInfo(name=self.name, price=self.price)


class CartItemResponse(BaseModel):
    id: int
    name: str
    price: float
    quantity: int

    @staticmethod
    def from_entity(entity: CartItem) -> CartItemResponse:
        return CartItemResponse(
            id=entity.id,
            name=entity.info.name,
            price=entity.info.price,
            quantity=entity.quantity,
        )


class CartResponse(BaseModel):
    id: int
    items: list[CartItemResponse]
    price: float

    @staticmethod
    def from_entity(entity: Cart) -> CartResponse:
        return CartResponse(
            id=entity.id,
            items=[
                CartItemResponse.from_entity(item) for item in entity.items.values()
            ],
            price=entity.price,
        )
