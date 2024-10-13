from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, Response
from pydantic import NonNegativeInt, PositiveInt

from lecture_2.hw.shop_api.app.schemas import (
    ItemRequest,
    ItemResponse,
    PatchItemRequest,
)
from lecture_2.hw.shop_api.app.storages import item_storage

ROOT = "/item"

router = APIRouter(prefix=ROOT)


@router.post(
    "/",
    status_code=HTTPStatus.CREATED,
)
async def add_item(request: ItemRequest, response: Response) -> ItemResponse:
    entity = item_storage.add(request.as_item_info())

    # as REST states one should provide uri to newly created resource in location header
    response.headers["location"] = f"{ROOT}/{entity.id}"

    return ItemResponse.from_entity(entity)


@router.get(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully returned requested item",
        },
        HTTPStatus.NOT_FOUND: {
            "description": "Failed to return requested item as one was not found",
        },
    },
)
async def get_item_by_id(id: int) -> ItemResponse:
    entity = item_storage.get_one(id)

    if not entity:
        raise HTTPException(
            HTTPStatus.NOT_FOUND,
            f"Request resource {ROOT}/{id} was not found",
        )

    return ItemResponse.from_entity(entity)


@router.get("/")
async def get_item_list(
    offset: Annotated[NonNegativeInt, Query()] = 0,
    limit: Annotated[PositiveInt, Query()] = 10,
    min_price: Annotated[NonNegativeInt | None, Query()] = None,
    max_price: Annotated[NonNegativeInt | None, Query()] = None,
    show_deleted: Annotated[bool, Query()] = False,
) -> list[ItemResponse]:
    return [
        ItemResponse.from_entity(e)
        for e in item_storage.get_many(
            offset, limit, min_price, max_price, show_deleted
        )
    ]


@router.put(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully updated or upserted pokemon",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify pokemon as one was not found",
        },
    },
)
async def put_item(
    id: int,
    request: ItemRequest,
) -> ItemResponse:
    entity = item_storage.replace(id, request.as_item_info())

    if entity is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource {ROOT}/{id} was not found",
        )

    return ItemResponse.from_entity(entity)


@router.patch(
    "/{id}",
    responses={
        HTTPStatus.OK: {
            "description": "Successfully patched item",
        },
        HTTPStatus.NOT_MODIFIED: {
            "description": "Failed to modify item as one was not found",
        },
    },
)
async def patch_item(id: int, info: PatchItemRequest) -> ItemResponse:
    entity = item_storage.update(id, info.as_patch_item_info())

    if entity is None:
        raise HTTPException(
            HTTPStatus.NOT_MODIFIED,
            f"Requested resource {ROOT}/{id} was not found",
        )

    return ItemResponse.from_entity(entity)


@router.delete("/{id}")
async def delete_item(id: int) -> Response:
    item_storage.delete(id)
    return Response("")
