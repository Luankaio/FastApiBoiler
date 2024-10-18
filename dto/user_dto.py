from pydantic import BaseModel, EmailStr, field_validator
import re
class UserDto(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator('username')
    def validate_username(cls, value):
        if not re.match(r'^[a-zA-Z\s]+$', value):
            raise ValueError('Username format invalid: Only letters are allowed')
        return value


