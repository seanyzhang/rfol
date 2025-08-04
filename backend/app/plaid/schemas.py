from pydantic import BaseModel
from uuid import UUID

class LinkTokenRequest(BaseModel):
    user_id: str

class LinkTokenResponse(BaseModel):
    link_token: str

class ExchangePublicTokenRequest(BaseModel):
    public_token: str

class ExchangePublicTokenResponse(BaseModel):
    message: str

class ItemOut(BaseModel):
    uuid: UUID
    plaid_item_id: str
    institution_name: str

class AccountOut(BaseModel):
    name: str
    uuid: UUID
    type: str
    plaid_item_uuid: UUID
    last_balance: float