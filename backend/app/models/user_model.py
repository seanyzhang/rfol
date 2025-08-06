from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base
from uuid import uuid4
from functools import cached_property

class User(Base):
    """
    SQLAlchemy model for storing user information.
    
    Attributes:
        id (int): Primary key, auto-incremented.
        uuid (UUID): Unique identifier for the user.
        username (str): Unique username for the user.
        hashed_email (str): Hashed email address for the user.
        encrypted_email (str): Encrypted email address for the user.
        first_name (str): User's first name.
        last_name (str): User's last name.
        hashed_password (str): Hashed password for the user.
        is_active (bool): Indicates if the user account is active.
        transactions (relationship): Relationship to the Transaction model.
        plaid_items (relationship): Relationship to the PlaidItem model.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    username = Column(String, unique=True, nullable=False, index=True)
    hashed_email = Column(String, unique=True, nullable=False, index=True)
    encrypted_email = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    transactions = relationship("Transaction", back_populates="user", cascade="all, delete-orphan")
    plaid_items = relationship("PlaidItem", back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(username={self.username}, uuid={self.uuid})>"

    @property
    def full_name(self) -> str:
        """Returns the user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @cached_property
    def decrypted_email(self) -> str:
        """Returns the user's decrypted email."""
        from app.auth.utils import decrypt_email
        return decrypt_email(self.encrypted_email) # type: ignore
