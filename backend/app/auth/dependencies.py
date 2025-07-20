from typing import Annotated
from fastapi import Cookie, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

import jwt, os
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv

from app.logger import logger
from app.auth.schemas import *
from app.db import db_dependency
from app.redis import redis_client as redis
from app.user.user_schema import UserOut
from app.user.user_crud import get_user_by_username

load_dotenv()

ACCESS_EXPIRY = int(os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES", "5"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: db_dependency
):
    logger.debug("Attempting to authenticate user from access token")
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            logger.warning("JWT payload missing 'sub' field")
            raise credentials_exception
        logger.debug(f"Token subject (username): {username}")
        token_data = TokenData(username=username)
    except InvalidTokenError as e:
        logger.warning(f"JWT decode failed: {e}")
        raise credentials_exception
    
    user = get_user_by_username(token_data.username, db)
    if not user:
        logger.warning(f"No user found for token subject: {token_data.username}")
        raise credentials_exception
    logger.info(f"Token valid — authenticated user '{user.username}'")
    return UserOut.model_validate(user)

async def get_current_active_user(
    current_user: Annotated[UserOut, Depends(get_current_user)]
):  
    is_active = bool(current_user.is_active)
    if not is_active:
        logger.warning("User is not active")
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user

async def get_current_session(
    db: db_dependency,
    session_id: Annotated[str | None, Cookie()] = None
) -> UserOut:
    if session_id is None:
        logger.warning("Session cookie missing")
        raise HTTPException(status_code=401, detail="Session cookie missing")
    
    logger.debug(f"Attempting to retrieve session for ID: {session_id}")
    username = await redis.get(f"session:{session_id}")
    
    if not username:
        logger.warning(f"No active session found for session ID: {session_id}")
        raise HTTPException(status_code=401, detail="Session expired/invalid")
    
    logger.debug(f"Session ID {session_id} mapped to username: {username}")
    user = get_user_by_username(username, db)

    if not user:
        logger.warning(f"User not found for username: {username}")
        raise HTTPException(status_code=404, detail="User not found")

    logger.info(f"Valid session session found for user {user.username}")
    return UserOut.model_validate(user)