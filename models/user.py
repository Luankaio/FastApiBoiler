from uuid import UUID
from pydantic import BaseModel, EmailStr
from datetime import datetime

class User(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    password: str
    created_at: datetime
    updated_at: datetime