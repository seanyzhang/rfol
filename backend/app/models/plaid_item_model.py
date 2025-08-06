from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base
from uuid import uuid4
from datetime import datetime, timezone

class PlaidItem(Base):
    """
    SQLAlchemy model for storing Plaid item information.
        
    Attributes:
        id (int): Primary key, auto-incremented.
        uuid (UUID): Unique identifier for the Plaid item.
        plaid_item_id (str): Unique Plaid item ID.
        plaid_access_token (str): Encrypted Plaid access token.
        institution_id (str): Plaid institution ID.
        institution_name (str): Name of the financial institution.
        is_active (bool): Indicates if the item is active.
        needs_reauth (bool): Indicates if the item needs re-authentication.
        last_error (str): Last error message from Plaid, if any.
        last_successful_sync (DateTime): Timestamp of the last successful sync with Plaid.
        user_uuid (UUID): Foreign key linking to the associated user.
        created_at (DateTime): Timestamp when the item was created.
        updated_at (DateTime): Timestamp when the item was last updated.
    """
    __tablename__ = "plaid_items"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    plaid_item_id = Column(String, unique=True, nullable=False)
    plaid_access_token = Column(String, nullable=False) 
    institution_id = Column(String, nullable=False)  
    institution_name = Column(String, nullable=False) 
    is_active = Column(Boolean, default=True)
    needs_reauth = Column(Boolean, default=False)  
    last_error = Column(String, nullable=True)
    last_successful_sync = Column(DateTime, nullable=True)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))
    
    user = relationship("User", back_populates="plaid_items")
    accounts = relationship("PlaidAccount", back_populates="plaid_item", cascade="all, delete-orphan")