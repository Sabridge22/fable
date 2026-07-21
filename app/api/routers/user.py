from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from sqlalchemy.orm import Session

from app.schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from app.services.user import UserNotFound, UserAlreadyExists, UserService

from app.db.session import get_db
from typing import Annotated

router = APIRouter(prefix="/users")

@router.post('', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.register_user(user_data=user_data)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))