import json
import os
from pathlib import Path
from mcp_server.tools.schemas.util import PlaidConnection
from mcp_server.services.keyring.auth import AuthHandler
from plaid import Environment

_STORAGE_DIR_ = Path.home() / "ttyf"
_CONNECTIONS_FILE = _STORAGE_DIR_ / "plaid_connections.json"
_CREDENTIALS_FILE = _STORAGE_DIR_ / "user_credentials.json"

def read_access_tokens() -> dict[str, PlaidConnection]:
    """
    Read the access tokens from the file.
    """
    with open(_CONNECTIONS_FILE, "r") as f:
        response_obj = {}
        connections = json.load(f)

        for connection in connections:
            id = connection["id"]
            access_token = AuthHandler.get_access_token(id)

            if not access_token:
                raise ValueError(f"Access token for {id} not found")

            response_obj[connection["name"]] = PlaidConnection(
                name=connection["name"],
                access_token=access_token,
                item_id=id,
            )
        

        return response_obj

def get_plaid_vars() -> tuple[str, str, Environment]:
    """
    Get the Plaid client ID and secret.
    """
    env = os.getenv("ENV", "DEV").lower()
    if env == "prod":
        return os.getenv("PLAID_CLIENT_ID"), os.getenv("PROD_PLAID_SECRET_KEY"), Environment.Production
    else:
        return os.getenv("PLAID_CLIENT_ID"), os.getenv("SANDBOX_PLAID_SECRET_KEY"), Environment.Sandbox