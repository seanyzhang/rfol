from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.logger import logger
from app.auth.authentication import authenticate_user, create_access_token
from app.db import db_dependency
from app.auth.schemas import Token

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/token")
async def login(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    logger.debug("Attempting to authenticate user")
    user = authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        logger.warning("Incorrect username or password")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    logger.info("User authenticated token created")
    access_token = create_access_token(
        data={"sub": user.username}
    )

    return Token(access_token=access_token, token_type="bearer")