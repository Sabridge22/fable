from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base

class UserORM(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(100), nullable=False)
    first_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    last_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    language_level: Mapped[str] = mapped_column(String(5), default="A1")
    message_count: Mapped[int] = mapped_column(Integer, default=0)
    mistakes_count: Mapped[int] = mapped_column(Integer, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    