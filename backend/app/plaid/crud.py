import datetime

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.users.schemas import UserOut
from app.plaid.schemas import ItemOut, AccountOut

from app.models.user_model import User
from app.models.plaid_account_model import PlaidAccount
from app.models.plaid_item_model import PlaidItem
from app.plaid.plaid import client
from app.db import db_dependency
from app.logger import logger


def create_plaid_item(
    item_id: str,
    access_token: str,
    current_user: UserOut,
    db: db_dependency   
):
    """
    Creates a new Plaid item and associates it with the current user.

    Args:
        item_id (str): The unique Plaid item ID.
        access_token (str): The Plaid access token for the item.
        current_user (UserOut): The currently authenticated user.
        db (db_dependency): The database dependency.

    Returns:
        ItemOut: The created Plaid item object.
    
    Raises:
        HTTPException: If there is an error creating the Plaid item or if the item already
                      exists for the user.
    """
    item_res = client.item_get({"access_token": access_token})
    institution_id = item_res["item"]["institution_id"]
    institution_res = client.institutions_get_by_id({"institution_id": institution_id})
    institution_name = institution_res["institution"]["name"]
    new_item = PlaidItem(
        plaid_item_id = item_id,
        plaid_access_token = access_token,
        institution_id = institution_id,
        institution_name = institution_name,
        user_uuid = str(current_user.uuid),
    )

    db.add(new_item)
    logger.debug(f"Attempting to add a connection from {institution_name} to the plaid account belonging to {current_user.username}")
    try:
        db.commit()
        db.refresh(new_item)
        logger.info(f"Successfully added connection from {institution_name} to {current_user.username}")
        return ItemOut(plaid_item_id=item_id, institution_name = institution_name, uuid=new_item.uuid) # type: ignore
    except IntegrityError as e:
        logger.warning(f"Unable to create connection to item due to: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    except Exception as e:
        logger.warning(f"Unable to create connection to item due to: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {e}")

def create_plaid_account(
    plaid_account_id: str,
    name: str,
    item: ItemOut,
    type: str,
    last_balance: float,
    subtype: str | None = None,
    mask: str | None = None,
    db: db_dependency,
):
    """
    Creates a new Plaid account and associates it with the specified Plaid item.

    Args:
        plaid_account_id (str): The unique Plaid account ID.
        name (str): The name of the account.
        item (ItemOut): The Plaid item to associate with the account.
        type (str): The type of the account (e.g., depository, credit).
        last_balance (float): The last known balance of the account.
        subtype (str | None): The subtype of the account (e.g., checking, savings). Defaults to None.
        mask (str | None): The last four digits of the account number. Defaults to None.
        db (db_dependency): The database dependency.

    Returns:
        AccountOut: The created Plaid account object.

    Raises:
        HTTPException: If there is an error creating the Plaid account or if the account already
                      exists for the item.
    """
    new_account = PlaidAccount(
        plaid_account_id = plaid_account_id,
        name = name,
        plaid_item_uuid = item.uuid,
        last_balance = last_balance,
        last_sync = datetime.datetime.now(datetime.timezone.utc).isoformat(),
        type = type,
        subtype = subtype
        mask = mask
    )

    db.add(new_account)
    logger.debug(f"Attempting to add a connection to {name} at {item.institution_name}")
    try:
        db.commit()
        db.refresh(new_account)
        logger.info(f"Successfully added account {name} at {item.institution_name}")
        return AccountOut(
            name=new_account.name,  # type: ignore
            uuid=new_account.uuid, # type: ignore
            type=new_account.type, # type: ignore
            plaid_item_uuid=item.uuid,
            last_balance = new_account.last_balance # type: ignore
            mask = new_account.mask # type: ignore
        )
    except IntegrityError as e:
        logger.warning(f"Unable to create connection to account due to: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    except Exception as e:
        logger.warning(f"Unable to create connection to account due to: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error: {e}")

def get_plaid_accounts(
    user: UserOut,
    db: db_dependency
):
    """
    Retrieve all Plaid accounts associated with the specified user.

    Args:
        user (UserOut): The user for whom to retrieve Plaid accounts.
        db (db_dependency): The database dependency.

    Returns:
        List[AccountOut]: A list of Plaid account objects associated with the user.
    """
    target_user_uuid = user.uuid
    results = (
        db.query(PlaidAccount)
        .join(PlaidItem, PlaidAccount.plaid_item_uuid == PlaidItem.uuid)
        .join(User, PlaidItem.user_uuid == User.uuid)
        .filter(User.uuid == target_user_uuid)
        .all()
    )

    return [
        AccountOut(
            name=account.name,  # type: ignore
            uuid=account.uuid, # type: ignore
            type=account.type, # type: ignore
            plaid_item_uuid=account.plaid_item_uuid, # type: ignore
            last_balance=account.last_balance # type: ignore
        ) for account in results
    ]