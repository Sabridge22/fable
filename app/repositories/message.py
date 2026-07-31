from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.message import MessageORM

class MessageRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user_id: str, content: str, response: str) -> MessageORM:
        new_message = MessageORM(user_id=user_id, content=content, response=response)
        self.db.add(new_message)
        return new_message