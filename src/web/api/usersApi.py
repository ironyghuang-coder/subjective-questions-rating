from datetime import timedelta
from sqlalchemy.orm import Session
from src.web.dto.userItem import UserItem
from fastapi import Depends, HTTPException, status
from fastapi import APIRouter
from src.web.config.database import get_db
from src.web.service import userService
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()

@router.get("/users/{user_id}")
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = userService.get_user_by_user_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="用户不存在")
    return db_user

@router.post("/users/")
async def create_user(user: UserItem, db: Session = Depends(get_db)):
    return userService.create_user(db=db, user=user)


@router.post("/users/login")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    """登录获取令牌"""
    user = userService.authenticate_by_username_password(db, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = userService.create_access_token(
        data={"sub": user.user_name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer", "exp": access_token_expires.seconds}