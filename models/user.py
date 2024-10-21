from typing import Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, ConfigDict, EmailStr
from datetime import datetime

class User(BaseModel):
    user_id: str
    username: str
    email: EmailStr
    password: str
    created_at: datetime
    updated_at: datetime
    is_active: Optional[bool] = None
    
    def serialize(self):
        return self.dict(exclude={'password'})

