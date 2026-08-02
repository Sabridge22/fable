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

    def create_message(self, message_data: MessageCreateSchema) -> MessageResponseSchema:
        if self.user_repository.get_by_id(user_id=message_data.user_id) is None:
            raise UserNotFound(f"User with id {message_data.user_id} not found")

        response_content = f"Echo: {message_data.content}"  # TODO: подключить Gemini
        
        message_orm = self.message_repository.create(user_id=message_data.user_id, content=message_data.content, response=response_content)

        self.db.commit()
        return MessageResponseSchema.model_validate(message_orm)