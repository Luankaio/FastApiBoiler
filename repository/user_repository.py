from bson.objectid import ObjectId
from db.database_connection import DataBaseConnection

mongo_uri = f"mongodb://"
database_name = "user"

class UserRepository:
    def __init__(self, uri: str, db: DataBaseConnection):
        self.collection = self.db['users'] 

    def create_user(self, user_data: dict) -> str:
        result = self.collection.insert_one(user_data)
        return result
    
    def get_user_by_id(self, user_id: str) -> dict:
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
        return user