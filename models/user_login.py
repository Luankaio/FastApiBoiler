from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class UserLogin(BaseModel):
    email: EmailStr
    password: str


