from mcp_server.storage.item import item_storage
from mcp_server.services.plaid.client import plaid_client
from plaid.model.accounts_get_request import AccountsGetRequest
from mcp_server.tools.schemas.tools import PlaidAccount, PlaidBalance, PlaidItem

def get_item_by_name(name: str) -> PlaidItem:
    """
    Retrieves a list of financial accounts.
    
    This function would normally connect to Plaid to fetch real account data,
    but for demonstration purposes, it returns dummy data.
    
    The response is cached per item_id using an LRU cache with max size of 128 items
    and a 30 minute TTL.
    
    Args:
        name: Optional name for a specific financial connection. This is what the name is saved as in the ttyf-cli
        
    Returns:
        A list of account objects containing account details
    """
    connection = item_storage.get_item(name)
    request = AccountsGetRequest(access_token=connection.access_token)
    item = plaid_client.client.accounts_get(request).to_dict()
    if item is None:
        return PlaidItem(name=name, accounts=[], access_token=None, item_id=None)

    parsed_accounts: list[PlaidAccount] = [
        PlaidAccount(
            account_id=account['account_id'],
            name=account['name'],
            mask=account['mask'],
            type=str(account['type']),
            subtype=str(account['subtype']),
            balances=PlaidBalance(
                available=account['balances']['available'],
                current=account['balances']['current'],
                limit=account['balances']['limit'],
                iso_currency_code=account['balances']['iso_currency_code'],
            ),
            holder_category=account['holder_category'] if 'holder_category' in account else None,
            official_name=account['official_name'] if 'official_name' in account else None,
        )
        for account in item['accounts']
    ]


    return PlaidItem(name=name, accounts=parsed_accounts, access_token=connection.access_token, item_id=connection.item_id)

def get_all_items() -> list[PlaidItem]:
    """
    Retrieves all financial accounts from all connections.
    
    This function fetches all accounts from all connections stored in the item storage.
    """
    items = item_storage.get_items()
    accs = []
    for item in items.values():
        accs.append(get_item_by_name(item.name))
    return accs

