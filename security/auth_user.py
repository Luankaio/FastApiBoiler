from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from models.user import User
from models.user_login import UserLogin
from repository.user_repository import UserRepository
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = 20  
REFRESH_TOKEN_EXPIRE_HOURS = 5
crypt_context = CryptContext(schemes=['sha256_crypt'])
bearer_scheme = HTTPBearer()

class UserUseCases:
    def __init__(self):
        self.user_repository = UserRepository()

    def user_login(self, user_login: UserLogin):
        user = self.user_repository.find_by_email(user_login.email)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail='Invalid email or password'
            )

        if not crypt_context.verify(user_login.password, user['password']):
            raise HTTPException(
                status_code=401,    
                detail='Invalid email or password'
            )

        access_token_exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        refresh_token_exp = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_HOURS)

        access_token_payload = {'sub': user['email'], 'exp': access_token_exp}
        refresh_token_payload = {'sub': user['email'], 'exp': refresh_token_exp}

        access_token = jwt.encode(access_token_payload, SECRET_KEY, algorithm=ALGORITHM)
        refresh_token = jwt.encode(refresh_token_payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'exp': access_token_exp.isoformat()
        }
    
    def create_access_token(self, data: dict):
        access_token_exp = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        data.update({"exp": access_token_exp})  # Adiciona a expiração ao payload
        return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

    def refresh_access_token(self, refresh_token: str):
        try:
            payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
            user = self.user_repository.find_by_email(payload['sub'])
            print(payload['sub'])
            if user is None:
                raise HTTPException(status_code=403, detail="Invalid refresh token")
            
            new_access_token = self.create_access_token(data={'sub': user['email']})

            return {'access_token': new_access_token}
        except JWTError:
            raise HTTPException(status_code=403, detail="Invalid refresh token")

    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
        token = credentials.credentials
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            raise HTTPException(
                status_code=401,
                detail='Invalid access token'
            )
        user = self.user_repository.find_by_email(data['sub'])

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        user_dict = user.__dict__ if isinstance(user, User) else user
        user_dict.pop('password', None) 
        return user_dict

    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
        self.get_current_user(credentials)
    

    def get_current_user_id(self, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
        user = self.get_current_user(credentials)
        return user['_id']

    def is_admin(self, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
        current_user = self.get_current_user(credentials)
        print(f"Current user role: {current_user.get('role')}") 
        if current_user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        if str(current_user["role"]) != "admin":
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return True
    