from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str

class UserInDB(UserBase):
    hashed_password: str
    uuid: UUID
    id: int

class UserCreate(UserBase):
    password: str