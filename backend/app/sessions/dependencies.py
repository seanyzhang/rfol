from typing import Annotated
from fastapi import Cookie, HTTPException

from app.logger import logger
from app.auth.schemas import *
from app.db import db_dependency
from app.redis import redis_client as redis
from app.users.schemas import UserOut
from app.users.crud import get_user_by_username

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