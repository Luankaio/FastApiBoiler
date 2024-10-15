from uuid import UUID
from bson.objectid import ObjectId
from fastapi import HTTPException, Response
from db.database_connection import DataBaseConnection

mongo_uri = f"mongodb://"
database_name = "user"

class UserRepository:
    def __init__(self, uri: str, db: DataBaseConnection):
        self.collection = self.db['users'] 
    
    async def create_user(self, user_data: dict) -> str:
        result = await self.collection.insert_one(user_data)
        return result
    
    async def get_user_by_id(self, user_id: UUID) -> dict:
        user = await self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            user['_id'] = str(user['_id'])
        return user
    
    async def delete_user(self, user_id: UUID):
        delete_result = await self.collection.delete_one({"__id": ObjectId(user_id)})
        if delete_result.deleted_count == 1:
            return Response(status_code=204, detail="NO CONTENT")
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
