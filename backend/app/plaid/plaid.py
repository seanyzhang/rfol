import plaid
import os
from plaid.api import plaid_api
from dotenv import load_dotenv

load_dotenv()

# Load Plaid API credentials from environment variables
client_id= os.getenv("PLAID_CLIENT_ID")
plaid_secret_id= os.getenv("PLAID_SANDBOX_ID") # Sandbox secret for testing

# Configure Plaid to use the Sandbox environment for development/testing
configuration = plaid.Configuration(
    host=plaid.Environment.Sandbox,
    api_key={
        'clientId': client_id,
        'secret': plaid_secret_id,
    }
)

# Create the API client configuration
api_client = plaid.ApiClient(configuration)

# Plaid client to interact with the API (e.g., link tokens, transactions)
client = plaid_api.PlaidApi(api_client)