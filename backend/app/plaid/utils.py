from uuid import UUID
from app.plaid.plaid import client
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.link_token_transactions import LinkTokenTransactions
from plaid.model.link_token_account_filters import LinkTokenAccountFilters
from plaid.model.depository_filter import DepositoryFilter
from plaid.model.depository_account_subtypes import DepositoryAccountSubtypes
from plaid.model.depository_account_subtype import DepositoryAccountSubtype
from plaid.model.credit_filter import CreditFilter
from plaid.model.credit_account_subtypes import CreditAccountSubtypes
from plaid.model.credit_account_subtype import CreditAccountSubtype

def create_link_token(user_uuid: UUID):
    """
    Creates a Plaid link token for the specified user.
    
    Args:
        user_uuid (UUID): The UUID of the user for whom the link token is created.
    
    Returns:
        str: The generated Plaid link token.
    """
    req = LinkTokenCreateRequest(
        user = LinkTokenCreateRequestUser(
            client_user_id=str(user_uuid)
        ),
        client_name= "rfol.io",
        products=["auth", "transactions"],
        country_codes=["US"],
        language="en",
        transactions=LinkTokenTransactions(
            days_requested=730
        ),
        account_filters=LinkTokenAccountFilters(
            depository=DepositoryFilter(
                account_subtypes=DepositoryAccountSubtypes([
                    DepositoryAccountSubtype('checking'),
                    DepositoryAccountSubtype('savings')
                ])
                ),
                credit=CreditFilter(
                account_subtypes=CreditAccountSubtypes([
                    CreditAccountSubtype('credit card')
                ])
            )
        )
    )
    res = client.link_token_create(req)
    return res.link_token