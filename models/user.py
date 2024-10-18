from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    password: str
    created_at: datetime
    updated_at: datetime

    

