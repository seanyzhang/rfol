from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator, model_validator

class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    @field_validator("username", "first_name", "last_name")
    @classmethod
    def no_spaces(cls, v: str) -> str:
        if " " in v:
            raise ValueError("Field cannot have a space")
        return v

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