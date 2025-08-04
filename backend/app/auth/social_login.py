from app.users.crud import get_user_by_email
from app.db import db_dependency

def google_sign_in(
    db: db_dependency,
    
):
    # TODO if user_email in DB, add google oauth2 info to account. else create new account with fetched data
    return 

def apple_sign_in():
    # same logic as google ssi
    return

def linkedin_sign_in(): # maybe switch to git or disc
    # same logic as google ssi
    return 