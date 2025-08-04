from pydantic import BaseModel, EmailStr, field_validator, model_validator

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str 

class PasswordUpdateRequest(BaseModel):
    current_pw: str
    new_pw: str
    confirm_new_pw: str

    @model_validator(mode='after')
    def pw_check(self) -> 'PasswordUpdateRequest':
        if self.new_pw != self.confirm_new_pw:
            raise ValueError('New password and confirmation do not match')
        if self.new_pw == self.current_pw:
            raise ValueError('New password cannot be the same as current password')
        
        return self
    

class PasswordUpdateResponse(BaseModel):
    message: str
    success: bool

class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class ForgotPasswordResponse(BaseModel):
    message: str
    success: bool

class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str
    
    @model_validator(mode='after')
    def pw_check(self) -> 'ResetPasswordRequest':
        if self.new_password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self
