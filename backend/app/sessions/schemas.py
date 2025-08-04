from pydantic import BaseModel

class SessionRequest(BaseModel):
    username: str 
    password: str

class SessionResponse(BaseModel):
    message: str
    success: bool