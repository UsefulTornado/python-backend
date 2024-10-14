from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt

from lecture_2.hw.shop_api.app.schemas import (
    CartResponse,
    ItemResponse,
)
from lecture_2.hw.shop_api.app.storages import cart_storage, item_storage

ROOT = "/cart"

router = APIRouter(prefix=ROOT)


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def add_cart(response: Response) -> CartResponse:
    entity = cart_storage.add()

    # as REST states one should provide uri to newly created resource in location header
    response.headers["location"] = f"{ROOT}/{entity.id}"

    return CartResponse.from_entity(entity)


@router.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested cart as one was not found",
        },
    },
)
async def get_cart_by_id(id: int) -> CartResponse:
    entity = cart_storage.get_one(id)

    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource {ROOT}/{id} was not found",
        )

    return CartResponse.from_entity(entity)


@router.get("/")
async def get_cart_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[NonNegativeInt | None, Query()] = None,
    max_price: Annotated[NonNegativeInt | None, Query()] = None,
    min_quantity: Annotated[NonNegativeInt | None, Query()] = None,
    max_quantity: Annotated[NonNegativeInt | None, Query()] = None,
) -> list[CartResponse]:
    return [
        CartResponse.from_entity(e)
        for e in cart_storage.get_many(
            offset, limit, min_price, max_price, min_quantity, max_quantity
        )
    ]


@router.post(
    "/{cart_id}/add/{item_id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully added item to cart",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to get item or cart",
        },
    },
)
async def add_item_to_cart(cart_id: int, item_id: int, response: Response):
    item = item_storage.get_one(item_id)
    if item is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Item with id {item_id} was not found",
        )

    cart = cart_storage.get_one(cart_id)
    if cart is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Cart with id {cart_id} was not found",
        )

    entity = cart_storage.add_item_to_cart(cart_id=cart_id, item=item)

    # as REST states one should provide uri to newly created resource in location header
    response.headers["location"] = f"{ROOT}/{cart_id}/{item_id}"

    return ItemResponse.from_entity(entity)
