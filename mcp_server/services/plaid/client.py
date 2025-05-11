import plaid
from plaid.configuration import Configuration
from plaid.api import plaid_api

from mcp_server.utils import get_plaid_vars

class PlaidServiceClient:
    def __init__(self):
        client_id, secret, env = get_plaid_vars()

        self.client_id = client_id
        self.secret = secret

        if not self.client_id or not self.secret:
            raise ValueError("PLAID_CLIENT_ID and PLAID_SECRET must be set")
        
        self.configuration = Configuration(
            host=env,
            api_key={
                'clientId': self.client_id,
                'secret': self.secret,
            }
        )
        self.client = plaid_api.PlaidApi(plaid.ApiClient(self.configuration))
            

def get_plaid_client() -> PlaidServiceClient:
    return PlaidServiceClient()


plaid_client = get_plaid_client()