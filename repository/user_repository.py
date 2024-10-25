from datetime import datetime
from uuid import UUID
from bson.objectid import ObjectId
from fastapi import HTTPException, Response
from pydantic import EmailStr
from db.database_connection import DataBaseConnection
from dto.paginated_response_dto import PaginatedResponse
from dto.pagination_dto import Pagination
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
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        user['_id'] = str(user['_id'])
        user.pop('password', None) 
        return user
    
    def get_all_users(self, pagination_params: Pagination):
        page = pagination_params.page 
        size = pagination_params.size 

        users = []
        cursor = self.collection.find({}).skip((page - 1) * size).limit(size)
        for user in cursor:
            user['_id'] = str(user['_id'])
            user_dict = user.__dict__ if isinstance(user, User) else user
            user_dict.pop('password', None)
            
            users.append(user_dict)
        return PaginatedResponse(total=10, page=page, page_size=size, data=users)
        #return users
    

    def update_user(self, user_id: str, update_data: dict):
        return self.collection.update_one(
            {"_id": ObjectId(user_id)}, 
            {"$set": update_data}
        )
    
    def soft_delete_user(self, user_id: str):
        return self.collection.update_one(
            {"_id": ObjectId(user_id)}, 
            {"$set": {"is_active": False,
                      "updated_at": datetime.now()}}
        )

    def delete_user(self, user_id: str):
        delete_result = self.collection.delete_one({"_id": ObjectId(user_id)})
        if delete_result.deleted_count == 1:
            return Response(status_code=204, detail="NO CONTENT")
        raise HTTPException(status_code=404, detail=f"Student {id} not found")
    
    def email_exists(self, email: EmailStr) -> bool:
        return bool(self.collection.find_one({"email": email}))


    def find_by_email(self, email: EmailStr):
        user = self.collection.find_one({"email": email})
        if user:
            user['_id'] = str(user['_id'])
            return user
        raise HTTPException(status_code=404, detail=f"Not Found")




