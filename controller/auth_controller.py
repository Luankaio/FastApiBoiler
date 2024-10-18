from uuid import UUID
from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models.user_login import UserLogin
from service.user_service import UserService
from security.auth_user import UserUseCases

user_use_cases = UserUseCases()

class UserAuthController:

    router = APIRouter(tags=['Auth'], prefix="/auth")
    
    @router.post("/login")
    def user_register(
        request_form_user: OAuth2PasswordRequestForm = Depends(),):  
        user = UserLogin(       
            email=request_form_user.username,
            password=request_form_user.password
        )

        auth_data = user_use_cases.user_login(user_login=user)

        return JSONResponse(
            content=auth_data,
            status_code=status.HTTP_200_OK
    )
