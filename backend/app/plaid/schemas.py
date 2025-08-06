from pydantic import BaseModel
from uuid import UUID

class LinkTokenRequest(BaseModel):
    """
    Model for the request to generate a Plaid link token.

    Attributes:
        user_id (str): The ID of the user for whom the link token is generated.
    """
    user_id: str

class LinkTokenResponse(BaseModel):
    """
    Model for the response containing the Plaid link token.
    
    Attributes:
        link_token (str): The generated Plaid link token.
    """
    link_token: str

class ExchangePublicTokenRequest(BaseModel):
    """
    Model for the request to exchange a public token for an access token.
    
    Attributes:
        public_token (str): The public token received from the Plaid link flow.
    """
    public_token: str

class ExchangePublicTokenResponse(BaseModel):
    """
    Model for the response after exchanging a public token for an access token.
    
    Attributes:
        message (str): A message indicating the result of the exchange."""
    message: str

class ItemOut(BaseModel):
    """
    Model for that reveals the details of a Plaid item.
    """
    uuid: UUID
    plaid_item_id: str
    institution_name: str

class AccountOut(BaseModel):
    """
    Model for that reveals the details of a Plaid account.
    """
    name: str
    uuid: UUID
    type: str
    plaid_item_uuid: UUID
    last_balance: float
    mask: str