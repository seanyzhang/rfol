from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from app.logger import logger
from app.db import db_dependency
from app.auth.dependencies import get_current_user
from app.auth.authentication import password_hash
from app.user.user_crud import create_user
from app.user.user_schema import UserCreate, UserOut
from app.models.user_model import User

router = APIRouter(
    prefix='/users',
    tags=['users']
)
    
@router.get("/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

@router.post("/create", response_model=UserOut)
async def create_new_user(user_data: UserCreate, db: db_dependency):
    logger.debug(f"Attempting to create user {user_data.username}")
    hashed_pw = password_hash(user_data.password)
    user = create_user(user_data, hashed_pw, db)
    logger.info(f"Successfully created user {user_data.username}")
    return user