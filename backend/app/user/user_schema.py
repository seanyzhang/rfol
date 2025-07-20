from uuid import UUID
from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str

class UserInDB(UserBase):
    hashed_password: str
    uuid: UUID
    id: int

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    uuid: UUID
    id: int
    is_active: bool
    model_config = {
        "from_attributes": True
    }