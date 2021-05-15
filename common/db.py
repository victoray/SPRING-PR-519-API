from pymongo import MongoClient

from settings import MONGODB_URL

client = MongoClient(MONGODB_URL)
