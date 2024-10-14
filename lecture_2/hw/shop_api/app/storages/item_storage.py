from typing import Iterable

from .models import Item, ItemInfo, PatchItemInfo


class ItemStorage:
    def __init__(self):
        self._data = dict[int, ItemInfo]()
        self._id_generator = self._int_id_generator()

    @staticmethod
    def _int_id_generator() -> Iterable[int]:
        i = 0
        while True:
            yield i
            i += 1

    def add(self, info: ItemInfo) -> Item:
        _id = next(self._id_generator)  # type: ignore
        self._data[_id] = info

        return Item(_id, info)

    def delete(self, id: int) -> None:
        if id in self._data:
            del self._data[id]

    def get_one(self, id: int) -> Item | None:
        if id not in self._data:
            return None

        return Item(id=id, info=self._data[id])

    def get_many(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: float | None = None,
        max_price: float | None = None,
        show_deleted: bool = False,
    ) -> Iterable[Item]:
        curr = 0

        def is_price_suitable(item_info):
            if min_price is None and max_price is None:
                return True
            elif min_price is None:
                return item_info.price <= max_price
            elif max_price is None:
                return item_info.price >= min_price
            else:
                return min_price <= item_info.price <= max_price

        for id, info in self._data.items():
            if (
                offset <= curr < offset + limit
                and is_price_suitable(info)
                and (show_deleted or not info.deleted)
            ):
                yield Item(id, info)

            curr += 1

    def replace(self, id: int, info: ItemInfo) -> Item:
        self._data[id] = info

        return Item(id=id, info=info)

    def update(self, id: int, patch_info: PatchItemInfo) -> Item | None:
        if id not in self._data:
            return None

        if patch_info.name is not None:
            self._data[id].name = patch_info.name

        if patch_info.price is not None:
            self._data[id].price = patch_info.price

        return Item(id=id, info=self._data[id])
