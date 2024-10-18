from uuid import UUID
from bson.objectid import ObjectId
from fastapi import HTTPException, Response
from pydantic import EmailStr
from db.database_connection import DataBaseConnection
from models.user import User

class UserRepository:
    def __init__(self):
        self.db = DataBaseConnection.db
        self.collection = self.db.collection
    
    def create_user(self, user_data: dict) -> str:
        result = self.collection.insert_one(user_data)
        return str(result)
    
    def get_user_by_id(self, user_id: str):
        user = self.collection.find_one({"_id": ObjectId(user_id)})
        return str(user)
    
    def get_all_users(self):
        users = []
        cursor = self.collection.find({})
        for user in cursor:
            user['_id'] = str(user['_id'])
            users.append(user)
        return users

    def delete_user(self, user_id: UUID):
        delete_result = self.collection.delete_one({"__id": ObjectId(user_id)})
        if delete_result.deleted_count == 1:
            return Response(status_code=204, detail="NO CONTENT")
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    
    def find_by_email(self, email: EmailStr):
        user = self.collection.find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])
            return user
        raise HTTPException(status_code=404, detail=f"Not Found")




