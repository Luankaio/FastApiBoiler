from uuid import UUID
from fastapi import HTTPException
from repository.user_repository import UserRepository
from models.user import User

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()


    async def create_user(self, user: User):
        if await self.email_exists(user):
            return HTTPException(status_code=400, detail="Email already registered")
        user_dict = user.__dict__
        return self.user_repository.create_user(user)

    def delete_user(self, user:User):
        #return await self.user_repository.delete
        pass

    async def find_user_by_id(self, id: UUID):
        return await self.user_repository.get_user_by_id(id)

    async def email_exists(self, user: User) -> bool:
        return await self.user_repository.find_one({"email": user.email})
    