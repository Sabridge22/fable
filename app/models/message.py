from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship
from .base import Base


class MessageORM(Base):
    __tablename__ = 'messages'

    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    response: Mapped[str] = mapped_column(Text, nullable=False)

    # связь с пользователем
    user: Mapped["UserORM"] = relationship(back_populates="messages")
    

