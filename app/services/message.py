from sqlalchemy.orm import Session
from app.repositories.message import MessageRepository
from app.schemas.message import MessageResponseSchema
from app.repositories.user import UserRepository
from app.services.user import UserNotFound
from app.services.llm import LLMService

class MessageService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.message_repository = MessageRepository(db)
        self.user_repository = UserRepository(db)
        self.llm_service = LLMService()

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

    def get_context(self, user_id: str, limit: int = 5) -> list[dict]:
        messages = self.message_repository.get_messages_by_user_id(user_id=user_id, limit=limit)
        
        context = []
        for msg in reversed(messages):
            context.append({
                "role": "model" if msg.role == 'assistant' else 'user',
                "parts": msg.content
            })
        return context

    def send_message(self, user_id: str, content: str) -> MessageResponseSchema:
        self.create_user_message(user_id=user_id, content=content)

        context = self.get_context(user_id=user_id)
        system_prompt = self.get_system_prompt()
        response_content = self.llm_service.generate_response(context=context, system_prompt=system_prompt)

        return self.create_assistant_message(user_id=user_id, content=response_content)

    def get_system_prompt(self) -> str:
        return(
            "Ты — дружелюбный репетитор английского языка. " 
            "Исправляй ошибки, хвали за успехи, всегда задавай вопросы. "
            "Отвечай на русском, если ученик пишет по-русски. "
            "Отвечай только на вопросы в последнем сообщении, если на предыдущие уже были даны ответы."
        )
    