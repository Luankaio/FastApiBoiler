from uuid import UUID
from fastapi import *
from fastapi.responses import JSONResponse
from models.user_login import UserLogin
from security.auth_user import UserUseCases

user_use_cases = UserUseCases()

class UserAuthController:

    router = APIRouter(tags=['Auth'], prefix="/auth")
    
    @router.post("/login")
    def user_auth(user_login: UserLogin):  
        user = UserLogin(       
            email=user_login.email,
            password=user_login.password
        )

        auth_data = user_use_cases.user_login(user_login=user)

        return JSONResponse(
            content=auth_data,
            status_code=status.HTTP_200_OK
    )

    @router.get("/protected")
    def protected_route(current_user: str = Depends(user_use_cases.verify_token)):
        return {"msg": "You are authorized", "user_id": current_user}

    @router.get("/me")
    def get_me(current_user: dict = Depends(user_use_cases.get_current_user)):
        return {"user": current_user}
    