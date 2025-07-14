from backend.db import db_dependency
from backend.schemas.user_schema import UserBase
from fastapi import HTTPException
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
import backend.models as models

def create_user(user: UserBase, hashed_pw: str, db: db_dependency):
    new_user = models.User(
        full_name = user.full_name.strip(),
        username = user.username.strip(),
        email = user.email.strip(),
        hashed_password = hashed_pw
    )

    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Email already in use")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    

def get_user_by_id(user_id: int, db: db_dependency):
    result = db.query(models.User).filter(models.User.id == user_id).first()
    if not result:
        raise HTTPException(status_code=404, detail='no user found with that ID')
    return result

def get_user_by_username(username: str, db: db_dependency):
    result = db.query(models.User).filter(models.User.username == username).first()
    if not result: 
        raise HTTPException(status_code=404, detail='no user found with that username')
    return result

def get_user_by_email(email: EmailStr, db: db_dependency):
    result = db.query(models.User).filter(models.User.email == email).first()
    if not result:
        raise HTTPException(status_code=404, detail='no user found with that email')
    return result
    
def get_user_by_query(query: int | str, db: db_dependency):
    if isinstance(query, int):
        user = get_user_by_id(query, db)
    elif isinstance(query, str):
        try:
            user = get_user_by_username(query, db)
        except HTTPException:
            user = get_user_by_email(query, db)
    else:
        raise HTTPException(status_code=400, detail='Non-Valid Query Type')
    
    if not user:
        raise HTTPException(status_code=404, detail='no user found')

    return user