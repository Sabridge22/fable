from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import MessageORM

class MessageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user_id: str, content: str, role: str) -> MessageORM:
        new_message = MessageORM(user_id=user_id, content=content, role=role)
        self.db.add(new_message)
        return new_message

    def get_messages_by_user_id(self, user_id: str, limit: int = 100, offset: int = 0) -> list[MessageORM]:
        stmt = select(MessageORM).where(MessageORM.user_id == user_id).limit(limit).offset(offset).order_by(MessageORM.created_at.desc())
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, message_id: str) -> MessageORM | None:
        return self.db.get(MessageORM, message_id)
    