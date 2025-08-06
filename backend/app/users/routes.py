from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi_limiter.depends import RateLimiter
from typing import Annotated
from pydantic import EmailStr

import datetime, secrets, json
from app.logger import logger
from app.db import db_dependency
from app.redis import redis_client as redis
from app.auth.dependencies import get_current_user
from app.auth.utils import password_hash, sanitize_pw
from app.auth.schemas import ForgotPasswordRequest, ForgotPasswordResponse, ResetPasswordRequest, PasswordUpdateResponse, ValidateResetTokenResponse
from app.users.crud import create_user, get_user_by_email, update_user_pw, get_user_by_username
from app.sessions.routes import check_session
from app.users.schemas import UserCreate, UserOut
from app.models.user_model import User

router = APIRouter(
    prefix='/users',
    tags=['users']
)
    
@router.get("/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    """
    Testing model. Get the currently authenticated user's details.
    
    Args:
        current_user (User): The currently authenticated user.
    """
    return current_user

@router.post("/create", response_model=UserOut, dependencies=[Depends(RateLimiter(times=6, minutes=1))])
async def create_new_user(
    user_data: UserCreate, 
    db: db_dependency
):
    """
    Create a new user in the database.
    
    Args:
        user_data (UserCreate): The user data to create.
        db (db_dependency): The database dependency.
    
    Returns:
        UserOut: The created user object.
    
    Raises:
        HTTPException: If the user creation fails due to validation errors or duplicate entries.
    """
    logger.debug(f"Attempting to create user {user_data.username}")
    if not sanitize_pw(user_data.password):
        logger.info(f"Failed to create user {user_data.username}")
        raise HTTPException(status_code=500, detail="Invalid password")
    
    user = create_user(user_data, db)
    logger.info(f"Successfully created user {user_data.username}")
    return user

@router.post("/forgot-password", dependencies=[Depends(RateLimiter(times=2, hours=1))])
async def forgot_password(
    req: ForgotPasswordRequest,
    background: BackgroundTasks,
    db: db_dependency
):
    """
    Handle forgot password requests by generating a reset token and sending it to the user's email.
    Args:
        req (ForgotPasswordRequest): The request containing the user's email.
        background (BackgroundTasks): Background tasks for sending emails.
        db (db_dependency): The database dependency.
    
    Returns:
        ForgotPasswordResponse: A response indicating the result of the password reset request.
    
    Raises:
        HTTPException: If the rate limit is exceeded or if there is an error processing the request
    """
    try:
        logger.debug(f"Password reset requested for email: {req.email}")

        pw_reset_key = f"pw_reset_rate:{req.email}"
        attempts = await redis.get(pw_reset_key)

        if attempts and int(attempts) >= 2:
            logger.warning(f"Rate limit exceeded for password reset: {req.email}")
            raise HTTPException(status_code=429, detail="Too many password reset attempts. Please try again later.")
        
        user = get_user_by_email(req.email, db)

        res = ForgotPasswordResponse(
            message="If an account exists with this email, you will receive a password reset link", 
            success=True
        )

        if not user:
            logger.warning(f"Password requested for non-existent email: {req.email}")
            await redis.incr(f"pw_reset_rate:{req.email}")
            await redis.expire(f"pw_reset_rate:{req.email}", 3600)
            return res
        
        existing_token_key = f"pw_reset:{user.username}"
        existing_token = await redis.get(existing_token_key)

        if existing_token:
            await redis.delete(f"pw_reset:{existing_token}")
            logger.info(f"Deleted existing reset token for user")

        reset_token = secrets.token_urlsafe(32)
        token_key = f"pw_reset:{reset_token}"
        token_data = {
            "username": user.username,
            "email": user.email,
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }

        async with redis.pipeline() as pipe:
            pipe.setex(token_key, 3600, json.dumps(token_data))
            pipe.setex(existing_token_key, 3600, reset_token)
            pipe.incr(pw_reset_key)
            pipe.expire(pw_reset_key, 3600)
            
            await pipe.execute()
        
        # Send email in background
        # TODO
        # background.add_task(
        #     send_reset_email,
        #     user.email,
        #     reset_token,
        #     user.username
        # )
        
        logger.info(f"Password reset token generated for user: {user.username}")
        
        return res
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error in forgot_password: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred processing your request")
    
@router.get("/validate-reset-token")
async def validate_reset_token(token: str):
    """
    Check if a reset token is valid.

    Args:
        token (str): The reset token to validate.

    Returns:
        dict: A dictionary indicating whether the token is valid and the associated email.
    
    Raises:
        HTTPException: If the token is invalid or expired.
    """
    token_key = f"pw_reset:{token}"
    token_data = await redis.get(token_key)
    
    if not token_data:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    data = json.loads(token_data)
    return ValidateResetTokenResponse(
        valid=True,
        email=data["email"],
        created_at=data["created_at"]
    )

@router.post("/reset-password", dependencies=[Depends(RateLimiter(times=2, hours=1))])
async def reset_password(
    req: ResetPasswordRequest,
    db: db_dependency
):
    """
    Reset the user's password using the provided reset token.
    
    Args:
        req (ResetPasswordRequest): The request containing the reset token and new password.
        db (db_dependency): The database dependency.
    
    Returns:
        PasswordUpdateResponse: A response indicating the result of the password reset.
    
    Raises:
        HTTPException: If the reset token is invalid or expired, or if there is an error processing the request.
    """
    try:
        logger.debug(f"Password reset attempt with token")

        token_key = f"pw_reset:{req.token}"
        token_data = await redis.get(token_key)
        
        if not token_data:
            logger.warning("Invalid or expired reset token")
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")

        data = json.loads(token_data)
        username = data["username"]
        
        user = get_user_by_username(username, db)
        if not user:
            logger.error(f"User {username} not found")
            raise HTTPException(status_code=404, detail="User not found")
        
        hashed_password = password_hash(req.new_password)
        update_user_pw(user.id, hashed_password, db) # type: ignore
        
        async with redis.pipeline() as pipe:
            pipe.delete(token_key)
            pipe.delete(f"user_pw_reset:{username}")

            cursor = 0
            while True:
                cursor, keys = await redis.scan(
                    cursor, 
                    match="session:*", 
                    count=100
                )
                for key in keys:
                    session_username = await redis.get(key)
                    if session_username == user.username:
                        pipe.delete(key)
                        logger.info(f"Invalidated session: {key}")
                if cursor == 0:
                    break
            
            await pipe.execute()
        
        logger.info(f"Password reset successful for user: {user.username}")

        return PasswordUpdateResponse(
            message="Password has been reset successfully. Please log in with your new password.",
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in reset_password: {str(e)}")
        raise HTTPException(status_code=500,detail="Failed to reset password")