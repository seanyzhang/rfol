from fastapi import APIRouter, HTTPException, Depends, Path
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from typing import Annotated
from app.auth.schemas import Token, PasswordUpdateRequest, PasswordUpdateResponse

from app.auth.utils import authenticate_user, create_access_token, verify_pw, password_hash
from app.auth.social_login import google_sign_in, apple_sign_in
from app.sessions.routes import check_session
from app.users.crud import get_user_by_username
from app.db import db_dependency
from app.logger import logger

# Auth-related routes (login and update password.)
router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

@router.post("/token/{provider}", dependencies=[Depends(RateLimiter(times=3, minutes=1))])
async def login(
    db: db_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    provider: Annotated[str, Path()] = "email"
):
    """
    Endpoint to authenticate user and return access token.
    
    Args:
        db (db_dependency): The database dependency.
        form_data (OAuth2PasswordRequestForm): The form data containing username and password.

    Returns:
        Token: A token object containing the access token and token type.
    
    Raises:
        HTTPException: If authentication fails or provider is invalid.
    """
    logger.debug("Attempting to authenticate user")

    if provider not in ["email", "google", "apple"]:
        logger.warning("Invalid authentication provider")

    if provider == "email":
        user = authenticate_user(db, form_data.username, form_data.password)
        
        if not user:
            logger.warning("Incorrect username or password")
            raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
        
    elif provider == "google":
        user = google_sign_in(db)
        if not user:
            logger.warning("Incorrect username or password")
            raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
        
    else:
        user = apple_sign_in(db)
        if not user:
            logger.warning("Incorrect username or password")
            raise HTTPException(status_code=401, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
        
    logger.info("User authenticated token created")
    access_token = create_access_token(
        data={"sub": user.username}
    )

    return Token(access_token=access_token, token_type="bearer")

@router.post("/update_password", dependencies=[Depends(RateLimiter(times=1, hours=1))])
async def update_pw(
    db: db_dependency,
    password_data: PasswordUpdateRequest,
    user_data: Annotated[dict, Depends(check_session)]
):
    """
    Endpoint to update user password.

    Args:
        db (db_dependency): The database dependency.
        password_data (PasswordUpdateRequest): The request data containing current and new passwords.
        user_data (dict): The user data from the session.
    
    Returns:
        PasswordUpdateResponse: A response indicating success or failure of the password update.
    
    Raises:
        HTTPException: If the current password is incorrect or if an error occurs during the update.
    """
    try:
        username = user_data.get("username")
        logger.info(f"Password update requested for user {username}")
        user = get_user_by_username(username, db) # type: ignore
        if not verify_pw(password_data.current_pw, user.hashed_password):  # type: ignore
            logger.warning(f"Failed password update attempt for user {username} - incorrect current password")
            raise HTTPException(status_code=401, detail="Current password is incorrect")

        new_hashed_pw = password_hash(password_data.new_pw)
        user.hashed_password = new_hashed_pw # type: ignore
        db.commit()

        logger.info(f"Password successfully updated for user {username}")
        res = PasswordUpdateResponse(message="Password updated successfully", success=True)
        return res

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating password: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to update password")