from datetime import datetime, timedelta, timezone

import jwt, os, re
from passlib.context import CryptContext
from dotenv import load_dotenv

from app.users.crud import get_user_by_query
from app.db import db_dependency

from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_EXPIRY = int(os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES", "5"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def validate_pw(password: str) -> bool:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return True if re.match(pattern, password) else False


def password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_pw(input_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(input_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_EXPIRY)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def authenticate_user(
    db: db_dependency, 
    query: str, 
    password: str
):
    user = get_user_by_query(query = query, db = db)
    if not user:
        return False
    if not verify_pw(password, user.hashed_password): # type: ignore
        return False
    return user 