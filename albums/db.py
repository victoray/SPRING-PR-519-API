from pymongo.collection import Collection
from pymongo.collation import Collation

from common.db import client
from settings import DATABASE

db = client[DATABASE]
ALBUM_COLLECTION = "album"
album_collection: Collection = db[ALBUM_COLLECTION]
album_collection.create_index(
    [("name", 1)],
    unique=1,
    collation=Collation(locale="en", strength=2),
)
SHARED_ALBUM_COLLECTION = "shared_album"
shared_album_collection: Collection = db[SHARED_ALBUM_COLLECTION]
shared_album_collection.create_index([("id", 1)], unique=1)
