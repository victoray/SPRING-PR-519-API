from pymongo.collection import Collection

from common.db import client
from settings import DATABASE

db = client[DATABASE]
BALANCE_COLLECTION = "photo"
photo_collection: Collection = db[BALANCE_COLLECTION]
photo_collection.create_index([("id", 1)], unique=True)
