from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import UserORM


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id: str) -> UserORM | None:
        return self.db.get(UserORM, user_id)
    
    def get_by_email(self, email: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.email == email)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def get_by_username(self, username: str) -> UserORM | None:
        stmt = select(UserORM).where(UserORM.username == username)
        return self.db.execute(stmt).scalar_one_or_none()
    
    def create(self, username: str, email: str, hashed_password: str) -> UserORM:
        new_user = UserORM(username=username, email=email, hashed_password=hashed_password)
        self.db.add(new_user)
        return new_user
    
    def update(self, user: UserORM, data: dict, ) -> UserORM:
        for key, value in data.items():
            if hasattr(user, key):
                setattr(user, key, value)

        return user
    
    def delete(self, user: UserORM) -> None:
        self.db.delete(user)


    def get_all(self, limit: int = 10, offset: int = 0) -> list[UserORM]:
        stmt = select(UserORM).limit(limit=limit).offset(offset=offset)
        return list(self.db.scalars(stmt).all())