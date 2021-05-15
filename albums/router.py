from contextlib import suppress
from typing import List

import pendulum
import pymongo
from bson import ObjectId
from fastapi import APIRouter, Body, Path, HTTPException
from pymongo.errors import DuplicateKeyError

from albums.db import album_collection
from albums.models import Album
from photos.db import photo_collection
from photos.utils import photos_to_dict

album_router = APIRouter(prefix="/albums")


@album_router.get("/", response_model=List[Album])
async def retrieve_albums(userId: str):
    query = {"userId": userId}
    result = album_collection.find(query)

    albums = []
    for doc in result:
        doc["id"] = str(doc.pop("_id"))
        doc["photos"] = doc.get("photos", [])
        albums.append(doc)

    return albums


@album_router.get("/{album_id}/", response_model=Album)
async def retrieve_album(album_id: str):
    query = {"_id": ObjectId(album_id)}
    result = album_collection.find_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="Album not found")

    result["id"] = str(result.pop("_id"))
    result["photos"] = photos_to_dict(
        photo_collection.find({"id": {"$in": result.get("photos", [])}})
    )
    return result


@album_router.post("/")
async def add_album(userId: str, body: dict):
    body["createdAt"] = body["updatedAt"] = pendulum.now()

    try:
        album_collection.insert_one({"userId": userId, **body})
    except DuplicateKeyError:
        raise HTTPException(
            status_code=400, detail="Album with the same name already exists"
        )

    return {"userId": userId, **body}


@album_router.post("/{album_id}/add")
async def add_photo_to_album(
    body: dict, album_id: str = Path(..., title="The album id")
):
    query = {"_id": album_id}
    update_query = {"$push": {"photos": body.pop("photoId")}}

    album_collection.update_one(query, update_query)

    return ""
