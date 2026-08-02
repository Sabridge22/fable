from sqlalchemy.orm import Session
from app.repositories.message import MessageRepository
from app.schemas.message import MessageCreateSchema, MessageResponseSchema
from app.repositories.user import UserRepository
from app.services.user import UserNotFound

class MessageService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.message_repository = MessageRepository(db)
        self.user_repository = UserRepository(db)

    def create_user_message(self, user_id: str, content: str) -> MessageResponseSchema:
        if self.user_repository.get_by_id(user_id=user_id) is None:
            raise UserNotFound(f"User with id {user_id} not found")
        
        message_orm = self.message_repository.create(user_id=user_id, content=content, role="user")

        self.db.commit()
        self.db.refresh(message_orm)
        return MessageResponseSchema.model_validate(message_orm)
    
    def create_assistant_message(self, user_id: str, content: str) -> MessageResponseSchema:
        if self.user_repository.get_by_id(user_id=user_id) is None:
            raise UserNotFound(f"User with id {user_id} not found")
        
        message_orm = self.message_repository.create(user_id=user_id, content=content, role="assistant")

        self.db.commit()
        self.db.refresh(message_orm)
        return MessageResponseSchema.model_validate(message_orm)

    def get_user_history(self, user_id: str, limit: int = 100, offset: int = 0) -> list[MessageResponseSchema]:
        messages = self.message_repository.get_messages_by_user_id(user_id=user_id, limit=limit, offset=offset)
        return [MessageResponseSchema.model_validate(message) for message in messages]

    def send_message(self, user_id: str, content: str) -> MessageResponseSchema:
        self.create_user_message(user_id=user_id, content=content)

        response_content = f"Echo: {content}"  # TODO: заменить на реальный вызов API

        return self.create_assistant_message(user_id=user_id, content=response_content)