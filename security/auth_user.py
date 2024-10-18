from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from models.user_login import UserLogin
from repository.user_repository import UserRepository
from decouple import config

SECRET_KEY = config('SECRET_KEY')
ALGORITHM = config('ALGORITHM')

crypt_context = CryptContext(schemes=['sha256_crypt'])
bearer_scheme = HTTPBearer()

class UserUseCases:
    def __init__(self):
        self.user_repository = UserRepository()


    def user_login(self, user_login: UserLogin, expires_in: int = 30):
        user = self.user_repository.find_by_email(user_login.email)

        if user is None:
            raise HTTPException(
                status_code=401,
                detail='Invalid email or password'
            )
        print(user['password'])
        print(user_login.password)
        print(crypt_context.hash(user['password']))

        if not crypt_context.verify(user_login.password, user['password']):
            raise HTTPException(
                status_code=401,    
                detail='Invalid username or password'
            )

        exp = datetime.now() + timedelta(minutes=190) #10 min, a partir de 180

        payload = {
            'sub': user['email'],
            'exp': exp
        }

        access_token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {
            'access_token': access_token,
            'exp': exp.isoformat()
        }
    
    def verify_token(self, credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
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
                status_code=401,
                detail='Invalid access token'
            )
        return user