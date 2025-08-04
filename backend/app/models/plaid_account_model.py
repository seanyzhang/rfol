from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db import Base
from uuid import uuid4

class PlaidAccount(Base):
    __tablename__ = "plaid_accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    plaid_account_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    official_name = Column(String, nullable=True)
    type = Column(String, nullable=False)
    subtype = Column(String, nullable=True)
    mask = Column(String, nullable=True)
    last_balance = Column(Float, nullable=True)
    last_sync = Column(DateTime, nullable=True)

    plaid_item_uuid = Column(UUID(as_uuid=True), ForeignKey('plaid_items.uuid'), nullable=False)
    plaid_item = relationship("PlaidItem", back_populates="accounts")