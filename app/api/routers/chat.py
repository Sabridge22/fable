import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.dependencies.auth import get_current_user
from app.models.user import UserORM
from app.services.message import MessageService
from app.schemas.message import MessageCreateSchema, MessageResponseSchema
from app.services.user import UserNotFound


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post('/', response_model=MessageResponseSchema)
def send_message(message_data: MessageCreateSchema, current_user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info(f"Сообщение от {current_user.email}: {message_data.content[:50]}...")
    service = MessageService(db)
    try:
        response = service.send_message(current_user.id, message_data.content)
        logger.info(f"Ответ отправлен пользователю {current_user.email}")
        return response
    except UserNotFound as e:
        logger.warning(f"Пользователь {current_user.email} не найден")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.get('/', response_model=list[MessageResponseSchema])
def get_history(limit: int = 100, offset: int = 0, current_user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    service = MessageService(db)
    return service.get_user_history(current_user.id, limit, offset)
        