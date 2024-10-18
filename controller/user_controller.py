from uuid import UUID
from fastapi import APIRouter
from dto.user_dto import UserDto
from service.user_service import UserService
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
 
    @router.put("/{id}")
    async def updateUser(): 
        return {"message": "Hello, World!"}