import logging

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from sqlalchemy.orm import Session

from app.schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from app.services.user import UserNotFound, UserAlreadyExists, UserService, PermissionDenied

from app.db.session import get_db
from typing import Annotated

from app.dependencies.auth import get_current_user
from app.models.user import UserORM


logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["User"])

@router.post('/register', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    logger.info(f"Попытка регистрации: {user_data.email}")
    service = UserService(db)
    try:
        user = service.register_user(user_data=user_data)
        logger.info(f"Пользователь зарегистрирован: {user.email} (ID: {user.id})")
        return user
    except UserAlreadyExists as e:
        logger.warning(f"Регистрация отклонена: {user_data.email} — {str(e)}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    

@router.get('/{user_id}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def get_user_by_id(user_id: str, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.get_user_by_id(user_id=user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

@router.get('/username/{username}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.get_user_by_username(username=username)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

@router.get('/email/{email}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.get_user_by_email(email=email)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    

@router.patch('/{user_id}', response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def update_user(user_id: str, update_data: UserUpdateSchema, current_user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)):
    logger.info(f"Попытка обновления пользователя: {current_user.email} (ID: {current_user.id})")
    service = UserService(db)
    try:
        user = service.update_user(user_id=user_id, current_user_id=current_user.id, update_data=update_data)
        logger.info(f"Данные пользователя обновлены: {user.email} (ID: {user.id})")
        return user
    except UserNotFound as e:
        logger.warning(f"Пользователь {user_id} не найден при попытке обновления")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserAlreadyExists as e:
        logger.warning(f"Конфликт при обновлении {user_id}: {str(e)}")
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except PermissionDenied as e:
        logger.warning(f"{current_user.email} пытался обновить {user_id} — нет прав")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: str, current_user: UserORM = Depends(get_current_user), db: Session = Depends(get_db)) -> None:
    logger.info(f"Попытка удаления пользователя: {user_id} от {current_user.email}")
    service = UserService(db)
    try:
        service.delete_user(user_id=user_id, current_user_id=current_user.id)
        logger.info(f"Пользователь {user_id} удалён")
    except UserNotFound as e:
        logger.warning(f"Пользователь {user_id} не найден при попытке удаления")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except PermissionDenied as e:
        logger.warning(f"{current_user.email} пытался удалить {user_id} — нет прав")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    