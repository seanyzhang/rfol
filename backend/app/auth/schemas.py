from pydantic import BaseModel, EmailStr, field_validator, model_validator

class Token(BaseModel):
    """
    Model representing an access token.

    Attributes:
        access_token (str): The JWT access token.
        token_type (str): The type of token, typically
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Model representing the data contained in a JWT token.

    Attributes:
        username (str): The username of the user associated with the token.
    """
    username: str 

class PasswordUpdateRequest(BaseModel):
    """
    Model for updating user password.
    
    Attributes:
        current_pw (str): The user's current password.
        new_pw (str): The new password to set.
        confirm_new_pw (str): Confirmation of the new password.
    
    Validations:
        - Ensures new password and confirmation match.
        - Ensures new password is not the same as the current password.
    """
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
    """
    Model for the response after updating the password.
    
    Attributes:
        message (str): A message indicating the result of the password update.
        success (bool): Indicates whether the password update was successful.
    """
    message: str
    success: bool

class ForgotPasswordRequest(BaseModel):
    """
    Model for requesting a password reset.
    
    Attributes:
        email (EmailStr): The email address of the user requesting the password reset.
    """
    email: EmailStr

class ForgotPasswordResponse(BaseModel):
    """
    Model for the response after requesting a password reset.
    
    Attributes:
        message (str): A message indicating the result of the password reset request.
        success (bool): Indicates whether the password reset request was successful.
    """
    message: str
    success: bool

class ResetPasswordRequest(BaseModel):
    """
    Model for resetting the password using a reset token.
    
    Attributes:
        token (str): The password reset token.
        new_password (str): The new password to set.
        confirm_password (str): Confirmation of the new password.
    
    Validations:
        - Ensures new password and confirmation match.
    """
    token: str
    new_password: str
    confirm_password: str
    
    @model_validator(mode='after')
    def pw_check(self) -> 'ResetPasswordRequest':
        if self.new_password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

class ValidateResetTokenResponse(BaseModel):
    """
    Model for the response after validating a reset token.
    
    Attributes:
        valid (bool): Indicates whether the reset token is valid.
        email (str): The email associated with the reset token.
        created_at (str): The timestamp when the reset token was created.
    """
    valid: bool
    email: str
    created_at: str