import jwt
import os
from dotenv import load_dotenv

from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.users.schemas import UserOut
from app.auth.schemas import *
from jwt.exceptions import InvalidTokenError

from app.users.crud import get_user_by_username
from app.db import db_dependency
from app.logger import logger


load_dotenv()

ACCESS_EXPIRY = int(os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES", "5"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], 
    db: db_dependency
): 
    """
    Validates JWT token and return current user

    Args:
        token (str): The JWT token from request header
        db (db_dependency): The database dependency
        
    Returns:
        UserOut: The user model with user details if token is valid

    Raises:
        HTTPException: If token is invalid or user not found
    """
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
    """
    Checks if the current user is active

    Args:
        current_user (UserOut): The current user object retrieved from `get_current_user`.
    Returns:
        UserOut: The current user object if the user is active.
    Raises:
        HTTPException: If user is not active
    """
    is_active = bool(current_user.is_active)
    if not is_active:
        logger.warning("User is not active")
        raise HTTPException(status_code=400, detail="Inactive User")
    return current_user