from datetime import datetime
from uuid import UUID, uuid4
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from pydantic import EmailStr
from repository.user_repository import UserRepository
from models.user import User
from dto.user_dto import UserDto
from dto.user_update_dto import UserUpdateDto
from security.auth_user import UserUseCases
crypt_context = CryptContext(schemes=['sha256_crypt'])

user_use_cases = UserUseCases()
class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, user_dto: UserDto):
        if self.user_repository.email_exists(user_dto.email):
            return HTTPException(status_code=400, detail="Email already registered")
        user = User(
            user_id=str(uuid4()),
            username=user_dto.username,
            email=user_dto.email,
            password=crypt_context.hash(user_dto.password),
            created_at=datetime.now(),
            updated_at=datetime.now(),
            is_active=True
        )
        user_dict = user.__dict__
        return self.user_repository.create_user(user_dict)

    def delete_user(self, user_id:str):
        return self.user_repository.delete_user()

    def update_user(self, user_id:str, user_update_dto:UserUpdateDto, current_user: dict = Depends(user_use_cases.get_current_user)):
        user = self.find_user_by_id(user_id)

        if(current_user["_id"] != user_id or current_user["role"]!= "admin"):
            raise HTTPException(status_code=403, detail="Insufficient permissions")

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        update_data = user_update_dto.dict(exclude_unset=True)
        update_data['updated_at'] = datetime.now()

        result = self.user_repository.update_user(user_id, update_data)

        if result.modified_count == 0:
            raise HTTPException(status_code=400, detail="No changes made or update failed")

        return self.find_user_by_id(user_id)
    
    def find_user_by_id(self, id: str):
        return self.user_repository.get_user_by_id(id)
    
    def get_all(self):
        return self.user_repository.get_all_users()