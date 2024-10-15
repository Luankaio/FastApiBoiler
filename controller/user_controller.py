from uuid import UUID
from fastapi import APIRouter
from models.user import User
from service.user_service import UserService

class CurriculumController:
    
    router = APIRouter(tags=['User'], prefix="/users")
    
    @router.post()
    async def createUser(user: User):
        return UserService.create_user(user)
    
    @router.get()
    async def getUser(id: UUID): 
        user = UserService.find_user_by_id(id)
        return {user}
    
    @router.delete()
    async def deleteUser(id: UUID): 
        return UserService.delete_user(id)
 
    @router.put()
    async def updateUser(): 
        return {"message": "Hello, World!"}