from fastapi import APIRouter, HTTPException, Depends
from typing import Annotated
from app.logger import logger
from app.plaid.plaid import client
from app.users.schemas import UserOut
from app.plaid.schemas import LinkTokenRequest, LinkTokenResponse, ExchangePublicTokenRequest, ExchangePublicTokenResponse
from app.plaid.crud import create_plaid_item, create_plaid_account, get_plaid_accounts
from app.plaid.utils import create_link_token
from app.sessions.dependencies import get_current_session
from app.db import db_dependency

router = APIRouter(
    prefix='/plaid',
    tags=['plaid']
)

@router.post("/create_link_token")
async def create_plaid_link_token(
    current_user: Annotated[UserOut, Depends(get_current_session)]
):
    try:
        link_token = create_link_token(current_user.uuid)
        return LinkTokenResponse(link_token=link_token)
    except Exception as e:
        logger.warning(str(e))
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/exchange_public_token")
async def exchange_public_token(
    req: ExchangePublicTokenRequest,
    current_user: Annotated[UserOut, Depends(get_current_session)],
    db: db_dependency
):
    try: 
        exchange_res = client.item_public_token_exchange(
            item_public_token_exchange_request={"public_token": req.public_token}
        )
        access_token = exchange_res.access_token
        item_id = exchange_res.item_id

        item = create_plaid_item(
            item_id= item_id, 
            access_token=access_token, 
            current_user=current_user, 
            db=db
        )

        accounts_response = client.accounts_get({
            "access_token": access_token
        })
        accounts = accounts_response['accounts']

        plaid_accounts = []
        for account in accounts:
            balances = account.get("balances", {})
            current_balance = balances.get("current")
            plaid_account = create_plaid_account(
                plaid_account_id=account.get('account_id'),
                name=account.get('name'),
                item=item,
                type=account.get('type'),
                subtype=account.get('subtype'),
                last_balance=current_balance,
                db=db
            )
            plaid_accounts.append(plaid_account)
            
        return ExchangePublicTokenResponse(message="Accounts linked successfully")
            
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/get_accounts")
async def get_accounts(
    current_user: Annotated[UserOut, Depends(get_current_session)],
    db: db_dependency
):
    try:
        res = get_plaid_accounts(current_user, db)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))