from typing import List

from fastapi import APIRouter

from chef.api.common import generic_get, generic_get_all, generic_delete
from chef.controllers import TagController
from chef.schemas import Tag

router = APIRouter()
tags = TagController()


@router.get("/")
async def get_tags() -> List[Tag]:
    return await generic_get_all(tags)


@router.get("/{item_id}")
async def get_tag(item_id: int) -> Tag:
    return await generic_get(tags, item_id)


@router.delete("/{item_id}")
async def delete_tag(item_id: int) -> None:
    return await generic_delete(tags, item_id)
