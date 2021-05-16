from contextlib import suppress
from typing import List

import pendulum
import pymongo
from bson import ObjectId
from fastapi import APIRouter, Body, Path, HTTPException
from pymongo.cursor import Cursor
from pymongo.errors import DuplicateKeyError
from starlette.requests import Request

from albums.db import album_collection, shared_album_collection
from albums.models import Album
from photos.db import photo_collection
from photos.utils import photos_to_dict

album_router = APIRouter(prefix="/albums")


def albums_to_dict(result: Cursor) -> List[dict]:
    albums = []
    for doc in result:
        doc["id"] = str(doc.pop("_id"))
        doc["photos"] = doc.get("photos", [])
        albums.append(doc)

    return albums


@album_router.get("/", response_model=List[Album])
async def retrieve_albums(userId: str):
    query = {"userId": userId}
    result = album_collection.find(query)

    return albums_to_dict(result)


@album_router.get("/shared/")
async def retrieve_shared_albums(userId: str):
    result = shared_album_collection.find({"userId": userId})
    shared_albums = [ObjectId(doc.pop("id")) for doc in result]

    return albums_to_dict(album_collection.find({"_id": {"$in": shared_albums}}))


@album_router.get("/{album_id}/")
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


@album_router.post("/{album_id}/add/")
async def add_photo_to_album(
    body: dict, album_id: str = Path(..., title="The album id")
):
    query = {"_id": ObjectId(album_id)}
    photo_id = body.pop("photoId")
    photo_query = {"id": photo_id}
    photo = photo_collection.find_one(photo_query) or {}
    update_query = {
        "$push": {"photos": photo_id},
        "$set": {"thumbnail": photo.get("urls", {}).get("regular")},
    }

    album_collection.update_one(query, update_query)

    return


@album_router.post("/import/")
async def import_album(body: dict, userId: str):
    try:
        shared_album_collection.insert_one(
            {"id": body.get("albumId"), "userId": userId}
        )
    except DuplicateKeyError:
        raise HTTPException(status_code=400, detail="Album already imported")
    return
