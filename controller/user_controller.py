from uuid import UUID
from fastapi import APIRouter, HTTPException
from dto.user_dto import UserDto
from service.user_service import UserService
from dto.user_update_dto import UserUpdateDto

user_service = UserService()

class UserController:

    router = APIRouter(tags=['User'], prefix="/users")
    
    @router.post("/")
    def createUser(user_dto: UserDto):
        return user_service.create_user(user_dto)
    
    @router.get("/{id}")
    def getUser(id: str): 
        user = user_service.find_user_by_id(id)
        return user
    
    @router.get("/")
    def get_all():
        users = user_service.get_all()
        return users
    
    @router.delete("/{id}")
    async def deleteUser(id: UUID): 
        return UserService.delete_user(id)
 
    @router.patch("/users/{user_id}")
    def update_user(user_id: str, user_update_dto: UserUpdateDto):
        try:
            updated_user = user_service.update_user(user_id, user_update_dto)
            return updated_user
        except HTTPException as e:
            raise HTTPException(status_code=e.status_code, detail=e.detail)