from datetime import datetime, timedelta, timezone

import jwt, os, re, hmac, hashlib
from cryptography.fernet import Fernet
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
HMAC_KEY = os.getenv("HMAC_SHA256_KEY")
FERNET_KEY = os.getenv("FERNET_KEY")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cipher = Fernet(FERNET_KEY)

def sanitize_pw(password: str) -> bool:
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return True if re.match(pattern, password) else False

def sanitize_email(email: str) -> str:
    return email.strip().lower()

def email_hash(email: str) -> str:
    return hmac.new(HMAC_KEY, email.lower().encode(), hashlib.sha256).hexdigest()

def encrypt_email(email: str) -> str:
    return cipher.encrypt(email.encode()).decode()

def decrypt_email(token: str) -> str:
    return cipher.decrypt(token.encode()).decode()

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