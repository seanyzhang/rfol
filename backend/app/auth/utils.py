import jwt 
import os
import re
import hmac
import hashlib
from dotenv import load_dotenv

from pydantic import EmailStr
from app.users.schemas import UserOut

from datetime import datetime, timedelta, timezone
from cryptography.fernet import Fernet
from passlib.context import CryptContext

from app.users.crud import get_user_by_query
from app.db import db_dependency

load_dotenv()

ACCESS_EXPIRY = int(os.getenv("ACCESS_TOKEN_EXPIRY_MINUTES", "5"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
HMAC_KEY = os.getenv("HMAC_SHA256_KEY")
FERNET_KEY = os.getenv("FERNET_KEY")

if not all([SECRET_KEY, HMAC_KEY, FERNET_KEY]):
    raise RuntimeError("Missing critical security environment variables.")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
cipher = Fernet(FERNET_KEY)

def sanitize_pw(password: str) -> bool:
    """
    Validate password strength. Criteria: 8 chars long, at least one uppercase, one lowercase, one digit, and one special character.

    Args:
        password (str): The password to validate.
    
    Returns:
        bool: True if the password meets the criteria, False otherwise.
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
    return True if re.match(pattern, password) else False

def sanitize_email(email: EmailStr) -> str:
    """"
    Sanitize email by stripping whitespace and converting to lowercase.

    Args:
        email (EmailStr): The email to sanitize.
    
    Returns:
        str: The sanitized email.
    """
    return email.strip().lower()

def email_hash(email: EmailStr) -> str:
    """
    Generate a SHA256 hash of the email for secure lookup and comparison.

    Args:
        email (EmailStr): The email to hash.
    
    Returns:
        str: The SHA256 hash of the email.
    """
    return hmac.new(HMAC_KEY, email.lower().encode(), hashlib.sha256).hexdigest()

def encrypt_email(email: str) -> str:
    """
    Encrypt the email using Fernet symmetric encryption.

    Args:
        email (str): The email to encrypt.  
    
    Returns:
        str: The encrypted email as a base64 encoded string.
    """
    return cipher.encrypt(email.encode()).decode()

def decrypt_email(token: str) -> str:
    """
    Decrypt the email using Fernet symmetric encryption.
    
    Args:
        token (str): The encrypted email token.
    
    Returns:
        str: The decrypted email.
    """
    return cipher.decrypt(token.encode()).decode()

def password_hash(password: str) -> str:
    """
    Hash the password using bcrypt.
    
    Args:
        password (str): The password to hash.
    
    Returns:
        str: The hashed password."""
    return pwd_context.hash(password)

def verify_pw(input_password: str, hashed_password: str) -> bool:
    """
    Verify the input password against the hashed password.
    
    Args:
        input_password (str): The password to verify.
        hashed_password (str): The hashed password to compare against.
    
    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(input_password, hashed_password)

def create_access_token(data: dict):
    """
    Create a JWT access token with the provided data.
    
    Args:
        data (dict): The data to encode in the token. Must include 'sub' for username.
    
    Returns:
        str: The encoded JWT token as a string."""
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
    """
    Authenticate a user by querying the database and verifying the password.
    
    Args:
        db (db_dependency): The database dependency.
        query (str): The query to find the user (username or email).
        password (str): The password to verify.
    
    Returns:
        UserOut: The authenticated user object if credentials are valid, otherwise None.
    """
    user = get_user_by_query(query = query, db = db)
    if not user:
        return False
    if not verify_pw(password, user.hashed_password): # type: ignore
        return False
    return UserOut.model_validate(user)