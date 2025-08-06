from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator, model_validator
from functools import cached_property
from app.auth.utils import decrypt_email  # adjust import as needed

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

class UserInDB(BaseModel):
    id: int
    uuid: UUID
    username: str
    first_name: str
    last_name: str
    hashed_password: str
    hashed_email: str
    encrypted_email: str
    is_active: bool

    model_config = {"from_attributes": True}

    @cached_property
    def decrypted_email(self) -> str:
        return decrypt_email(self.encrypted_email)

class UserCreate(UserBase):
    password: str

class UserOut(UserBase):
    uuid: UUID
    id: int
    is_active: bool
    model_config = {"from_attributes": True}