from pydantic import BaseModel
from typing import Optional

class UserUpdateDto(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
