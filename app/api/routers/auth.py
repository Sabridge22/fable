from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.user import UserService, UserNotFound
from app.core.security import create_access_token
from app.schemas.user import UserResponseSchema
from app.dependencies.auth import get_current_user
from app.models.user import UserORM

router = APIRouter(prefix='/auth', tags=["Authentication"])

@router.post('/login')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    service = UserService(db)
    try:
        user = service.get_user_orm_by_email(form_data.username)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})

    if not service.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password", headers={"WWW-Authenticate": "Bearer"})

    access_token = create_access_token(data={'sub': user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get('/me', response_model=UserResponseSchema)
async def get_me(current_user: UserORM = Depends(get_current_user)):
    return current_user

