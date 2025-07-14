from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from backend.db import db_dependency
from backend.utils.authentication import password_hash, get_current_user
from backend.crud.user_crud import create_user
from backend.schemas.user_schema import UserCreate, UserInDB
import backend.models as models

router = APIRouter(
    prefix='/users',
    tags=['users']
)
    
@router.get("/me")
async def read_users_me(current_user: Annotated[models.User, Depends(get_current_user)]):
    return current_user

@router.post("/", response_model=UserInDB)
async def create_new_user(user_data: UserCreate, db: db_dependency):
    hashed_pw = password_hash(user_data.password)
    user = create_user(user_data, hashed_pw, db)
    return user