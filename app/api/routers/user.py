from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from sqlalchemy.orm import Session

from app.schemas.user import UserCreateSchema, UserResponseSchema, UserUpdateSchema
from app.services.user import UserNotFound, UserAlreadyExists, UserService

from app.db.session import get_db
from typing import Annotated

router = APIRouter(prefix="/users", tags=["Users"])

@router.post('/register', response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(user_data: UserCreateSchema, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.register_user(user_data=user_data)
    except UserAlreadyExists as e:
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
def update_user(user_id: str, update_data: UserUpdateSchema, db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        return service.update_user(user_id=user_id, update_data=update_data)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
