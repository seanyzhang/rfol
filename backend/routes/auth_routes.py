from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from backend.crud.user_crud import get_user_by_email, get_user_by_username
from backend.utils.authentication import verify_pw, create_access_token
from backend.db import db_dependency
from backend.schemas.token_schema import Token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/token")
async def login(
    db: db_dependency,
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = None
    try:
        user = get_user_by_username(form_data.username, db)
    except HTTPException:
        try:
            user = get_user_by_email(form_data.username, db)
        except HTTPException:
            raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not verify_pw(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    access_token = create_access_token(data={"sub": user.username})
    
    return Token(access_token=access_token, token_type= "bearer")