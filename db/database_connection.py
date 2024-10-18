from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()


class DataBaseConnection:

    
    uri = os.getenv('DB_URI')
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client.listen_db
    collection = db["users"]