from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from uuid import uuid4
from app.db import Base

class UserSalary(Base):
    __tablename__ = "UserSalaries"

    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4)
    user_uuid = Column(UUID(as_uuid=True), ForeignKey('users.uuid'), nullable=False)
    user = relationship("User", back_populates="salaries")
    salary_amount = Column(Integer, nullable=False)
    currency = Column(String(3), nullable=False)  
    is_active = Column(Boolean, default=True)  