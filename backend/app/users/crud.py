from app.db import db_dependency
from sqlalchemy.orm import Session
from app.users.schemas import UserCreate
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from app.users.schemas import UserOut
from app.models.user_model import User
from app.logger import logger
from app.auth.utils import sanitize_email, password_hash, email_hash, encrypt_email, decrypt_email

def create_user(
    user: UserCreate, 
    db: Session
):
    hashed_pw = password_hash(user.password)
    sanitized_email = sanitize_email(user.email)
    hashed_email = email_hash(sanitized_email)
    encrypted_email = encrypt_email(sanitized_email)

    new_user = User(
        first_name = user.first_name.strip().lower(),
        last_name = user.last_name.strip().lower(),
        username = user.username.strip().lower(),
        hashed_email = hashed_email,
        encrypted_email = encrypted_email,
        hashed_password = hashed_pw
    )

    db.add(new_user)
    logger.debug(f"Attempting to add user {new_user.username} to db")
    try:
        db.commit()
        db.refresh(new_user)
        logger.info(f"Successfully commited user {new_user.username} to db")
        return UserOut(
            first_name=new_user.first_name, # type: ignore
            last_name=new_user.last_name, # type: ignore
            username=new_user.username, # type: ignore
            email=decrypt_email(new_user.encrypted_email), # type: ignore
            uuid=new_user.uuid, # type: ignore
            id=new_user.id, # type: ignore
            is_active=new_user.is_active # type: ignore
        )
    except IntegrityError as e:
        logger.warning(f"Unable to create user due to: {e}")
        db.rollback()
        if "email" in str(e.orig).lower():
            logger.warning("Unable to create user due to duplicate email")
            raise HTTPException(status_code=409, detail="Email already in use")
        elif "username" in str(e.orig).lower():
            logger.warning("Unable to create user due to duplicate username")
            raise HTTPException(status_code=409, detail="Username already taken")
        else:
            logger.warning("Unable to create user due to duplicate credentials")
            raise HTTPException(status_code=409, detail="User with given credentials already exists")
    except Exception as err:
        db.rollback()
        logger.warning(f"Unable to create user due to error: {err}")
        raise HTTPException(status_code=500, detail=f"Error: {err}")
    

def get_user_by_id(user_id: int, db: db_dependency) -> User:
    logger.debug(f"searching for user of id: {user_id}")
    result = db.query(User).filter(User.id == user_id).first()
    if not result:
        logger.warning(f"No user with id {user_id} found")
        raise HTTPException(status_code=404, detail='no user found with that ID')
    logger.info(f"User found")
    return result

def get_user_by_username(username: str, db: db_dependency) -> User:
    logger.debug(f"searching for user of username: {username}")
    result = db.query(User).filter(User.username == username).first()
    if not result: 
        logger.warning(f"No user with username {username} found")
        raise HTTPException(status_code=404, detail='no user found with that username')
    logger.info(f"User found")
    return result

def get_user_by_email(email: EmailStr, db: db_dependency) -> User:
    logger.debug(f"searching for user of email: {email}")
    sanitized_email = sanitize_email(email)
    target_hashed_email = email_hash(sanitized_email)
    result = db.query(User).filter(User.hashed_email == target_hashed_email).first()
    if not result:
        logger.warning(f"No user with email {email} found")
        raise HTTPException(status_code=404, detail='no user found with that email')
    logger.info(f"User found")
    return result
    
def get_user_by_query(query: int | str, db: db_dependency) -> User:
    user = None
    logger.debug(f"searching for user by query: {query}")
    if isinstance(query, int):
        logger.debug("Searching via id")
        try:
            user = get_user_by_id(query, db)
            if user: logger.info("User found via ID")
        except HTTPException:
            logger.debug("No user found via id")
            pass
    elif isinstance(query, str):
        logger.debug("Searching via username")
        try:
            user = get_user_by_username(query, db)
            if user: logger.info("User found via username")
            else: logger.debug("no user by username")
        except HTTPException:
            logger.debug("Searching via email")
            try:
                sanitized = sanitize_email(query)
                user = get_user_by_email(sanitized, db)
                if user: logger.info("User found via email")
                else: logger.info("no user found by email")
            except HTTPException:
                pass
    
    if not user:
        logger.warning("No user found")
        raise HTTPException(status_code=404, detail='User not found')

    logger.info(f"returning user {user.username}")
    return user

def update_user_pw(query: int | str, hashed_pw: str, db: db_dependency):
    user = get_user_by_query(query, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = hashed_pw # type: ignore
    db.commit()
    db.refresh(user)
    return user