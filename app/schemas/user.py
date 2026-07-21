from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=100)

class UserResponseSchema(BaseModel):
    id: str
    username: str
    email: EmailStr
    language_level: str
    message_count: int
    mistakes_count: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class UserUpdateSchema(BaseModel):
    username: str | None = None
    language_level: str | None = None
    is_active: bool | None = None