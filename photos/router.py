from contextlib import suppress
from typing import List

import pendulum
import pymongo
from fastapi import APIRouter, Body, Path
from pymongo.cursor import Cursor
from pymongo.errors import DuplicateKeyError

from photos.db import photo_collection
from photos.utils import photos_to_dict

photo_router = APIRouter(prefix="/photos")


@photo_router.get("/{user_id}/")
async def retrieve_photos(user_id: str = Path(..., title="The user id of photos")):
    query = {"userId": user_id}
    result = photo_collection.find(query)

    return photos_to_dict(result)


@photo_router.get("/{user_id}/recent/")
async def retrieve_recent_photos(
    user_id: str = Path(..., title="The user id of photos")
):
    query = {"userId": user_id}
    result = (
        photo_collection.find(query).sort("createdAt", pymongo.DESCENDING).limit(20)
    )

    return photos_to_dict(result)


@photo_router.post("/")
async def add_photo(userId: str, body: dict):
    body["createdAt"] = body["updatedAt"] = pendulum.now()
    with suppress(DuplicateKeyError):
        photo_collection.insert_one({"userId": userId, **body})

    return {"userId": userId, **body}
