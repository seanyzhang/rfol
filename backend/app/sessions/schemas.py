from pydantic import BaseModel

class SessionRequest(BaseModel):
    """
    Model for the request to create a new session.
    
    Attributes:
        username (str): The username of the user creating the session.
        password (str): The password of the user creating the session.
    """
    username: str 
    password: str

class SessionResponse(BaseModel):
    """
    Model for the response after creating a session.

    Attributes:
        message (str): A message indicating the result of the session creation.
        success (bool): Indicates whether the session creation was successful.
    """
    message: str
    success: bool