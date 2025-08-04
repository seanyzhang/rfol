import plaid
from plaid.api import plaid_api

from dotenv import load_dotenv
import os
load_dotenv()

client_id= os.getenv("PLAID_CLIENT_ID")
plaid_secret_id= os.getenv("PLAID_SANDBOX_ID")
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': client_id,
        'secret': plaid_secret_id,
    }
)

api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)