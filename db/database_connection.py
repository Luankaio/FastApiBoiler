from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from decouple import config


class DataBaseConnection:

    uri = config('DB_URI')
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client.listen_db
    collection = db["users"]