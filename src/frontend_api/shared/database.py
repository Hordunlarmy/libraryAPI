from pymongo import MongoClient
from decouple import config


MONGO_URI = config("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client.frontend_db
