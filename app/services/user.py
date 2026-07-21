from sqlalchemy.orm import Session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserNotFound(Exception):
    """Пользователь не найден"""
    ...

class UserAlreadyExists(Exception):
    """Пользователь уже существует"""
    ...


class UserService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.user_repository = UserRepository(db)


    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)


    def register_user(self, user_data: UserCreateSchema) -> UserResponseSchema:
        if self.user_repository.get_by_username(user_data.username) is not None:
            raise UserAlreadyExists("Username already taken")
        if self.user_repository.get_by_email(user_data.email) is not None:
            raise UserAlreadyExists("Email already taken")
        
        hashed_password = self.hash_password(user_data.password)
        new_user = self.user_repository.create(username=user_data.username, email=user_data.email, hashed_password=hashed_password)
        self.db.commit()
        self.db.refresh(new_user) # для подгрузки полей, генерируемых в бд
        return UserResponseSchema.model_validate(new_user)


    def get_user_by_id(self, user_id: str) -> UserResponseSchema:
        user = self.user_repository.get_by_id(user_id=user_id)
        if user is None:
            raise UserNotFound("User not found")
        return UserResponseSchema.model_validate(user)


    def get_user_by_username(self, username: str) -> UserResponseSchema:
        user = self.user_repository.get_by_username(username=username)
        if user is None:
            raise UserNotFound("User not found")
        return UserResponseSchema.model_validate(user)


    def get_user_by_email(self, email: str) -> UserResponseSchema:
        user = self.user_repository.get_by_email(email=email)
        if user is None:
            raise UserNotFound("User not found")
        return UserResponseSchema.model_validate(user)
        


    def update_user(self):
        ...
    

    def delete_user(self):
        ...


    def get_all_users(self):
        ...
