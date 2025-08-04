from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base
from uuid import uuid4
from datetime import datetime, timezone

class PlaidItem(Base):
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