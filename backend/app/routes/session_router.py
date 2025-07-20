from fastapi import APIRouter, HTTPException, Depends, Response, Cookie
from fastapi_limiter.depends import RateLimiter
from typing import Annotated

import uuid
from app.logger import logger
from app.auth.dependencies import get_current_active_user
from app.redis import redis_client as redis
from app.db import db_dependency
from app.user.user_schema import UserOut
from app.user.user_crud import get_user_by_username

from dotenv import load_dotenv
import os
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

router = APIRouter(
    prefix='/session',
    tags=['session']
)

@router.post("/create", dependencies=[Depends(RateLimiter(times=3, minutes=1))])
async def create_session(
    response: Response,
    current_user: Annotated[UserOut, Depends(get_current_active_user)]
):
    logger.debug(f"Creating session for user: {current_user.username}")

    session_id = str(uuid.uuid4())
    await redis.setex(f"session:{session_id}", 3600, str(current_user.username))

    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=True,
        samesite="strict",
        max_age=3600 
    )

    logger.info(f"Session created for user {current_user.username}")
    return {"message": "Session created"}

@router.get("", dependencies=[Depends(RateLimiter(times=3, minutes=1))])
async def check_session(db: db_dependency, session_id: str | None = Cookie(default=None)):
    logger.debug("Checking session id")
    if session_id is None:
        logger.warning("no session cookie")
        raise HTTPException(status_code=401, detail="Missing session cookie")
    
    logger.debug("Checking Redis for session id")
    username = await redis.get(f"session:{session_id}")
    if not username: 
        logger.warning("invalid or expired session")
        raise HTTPException(status_code=401, detail="Invalid or expired session")
    
    logger.debug("Searching for userdata")
    user = get_user_by_username(username, db)
    logger.info(f"Session verified for user {user.username}")

    return {
        "uuid": str(user.uuid),
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

@router.post("/logout")
async def logout(response: Response, session_id: str):
    logger.debug("logging out")
    response.delete_cookie(key="session_id")
    await redis.delete(f"session:{session_id}")
    logger.info("Successfully logged out")
    return {"logged out"}