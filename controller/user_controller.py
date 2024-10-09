from fastapi import APIRouter
from models.user import User
from service.user_service import UserService

class CurriculumController:
    
    router = APIRouter(tags=['User'], prefix="/users")
    
    @router.post()
    async def createUser(user: User): 
        return UserService.create_user(user)
    
    @router.get()
    async def getUser(): 
        return {"message": "Hello, World!"}
    
    @router.delete()
    async def deleteUser(): 
        return {"message": "Hello, World!"}
 
    @router.put()
    async def updateUser(): 
        return {"message": "Hello, World!"}