from datetime import datetime
from uuid import UUID, uuid4
from passlib.context import CryptContext
from repository.user_repository import UserRepository
from models.user import User
from dto.user_dto import UserDto

crypt_context = CryptContext(schemes=['sha256_crypt'])

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, user_dto: UserDto):
        #if await self.email_exists(user):
        #    return HTTPException(status_code=400, detail="Email already registered")
        user = User(
            _id=str(uuid4()),
            username=user_dto.username,
            email=user_dto.email,
            password=crypt_context.hash(user_dto.password),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        user_dict = user.__dict__
        return self.user_repository.create_user(user_dict)

    def delete_user(self, user:User):
        return self.user_repository.delete_user()
        pass

    def find_user_by_id(self, id: str):
        return self.user_repository.get_user_by_id(id)

    def email_exists(self, user: User) -> bool:
        return self.user_repository.find_one({"email": user.email})
    
    def get_all(self):
        return self.user_repository.get_all_users()