from typing import Any
from mcp_server.enums.plaid import PlaidAccountType
from mcp_server.tools.get_accounts import get_all_items
from mcp_server.tools.schemas.io import GetNetWorthResponse, NetWorthAssetBreakdown, NetWorthLiabilityBreakdown
from mcp_server.tools.schemas.tools import PlaidAccount

def _is_liability(account_type: str) -> bool:
    return account_type == PlaidAccountType.CREDIT.value or account_type == PlaidAccountType.LOAN.value

def _is_asset(account_type: str) -> bool:
    return account_type == PlaidAccountType.DEPOSITORY.value or account_type == PlaidAccountType.INVESTMENT.value

def get_net_worth() -> GetNetWorthResponse:
    """
    Calculates total net worth by summing assets and subtracting liabilities. 
    This is the only tool that you need to get net worth.
    
    Returns:
        A dictionary containing net worth information, including total assets,
        total liabilities, and overall net worth
    """   
    items = get_all_items()
    
    # Calculate assets (positive balances) and liabilities (negative or credit accounts)
    assets: list[PlaidAccount] = []
    liabilities: list[PlaidAccount] = []
    
    for item in items:
        for account in item.accounts:
            account_type = account.type

            match account_type:
                case _ if _is_liability(account_type):
                    liabilities.append(account)
                case _ if _is_asset(account_type):
                    assets.append(account)
        
    # Calculate totals
    total_assets = sum(asset.balances.current for asset in assets)
    total_liabilities = sum(liability.balances.current for liability in liabilities)
    net_worth = total_assets - total_liabilities
    
    return GetNetWorthResponse(
        assets=NetWorthAssetBreakdown(
            accounts=assets,
            total=total_assets
        ),
        liabilities=NetWorthLiabilityBreakdown(
            accounts=liabilities,
            total=total_liabilities
        ),
        net_worth=net_worth
    )