from mcp_server.enums.plaid import PlaidAccountSubtype, PlaidAccountType
from mcp_server.tools.get_accounts import get_all_items
from mcp_server.tools.schemas.io import CreditCardBreakdown, GetCurrentLiabilitiesResponse, LoanBreakdown
from mcp_server.tools.schemas.tools import PlaidCreditCard, PlaidLoan

def _is_credit_card(account_type: str, account_subtype: str) -> bool:
    return account_type == PlaidAccountType.CREDIT.value and account_subtype == PlaidAccountSubtype.CREDIT_CARD.value

def _is_loan(account_type: str) -> bool:
    return account_type == PlaidAccountType.LOAN.value

def get_current_liabilities() -> GetCurrentLiabilitiesResponse:
    """
    Retrieves current liabilities such as credit card balances and overdrafts.

        
    Returns:
        A dictionary containing liability information grouped by type
    """
    # Get accounts using the global get_accounts function
    items = get_all_items()
    
    # Filter and categorize liabilities
    credit_card_liabilities: list[PlaidCreditCard] = []
    loan_liabilities: list[PlaidLoan] = []
    
    for item in items:
        for account in item.accounts:
            account_type = account.type
            account_subtype = account.subtype

            if account.balances.current > 0:
                if _is_credit_card(account_type, account_subtype):
                    credit_card_liabilities.append(PlaidCreditCard(
                        account_id=account.account_id,
                        name=account.name,
                        mask=account.mask,
                        type=account.type,
                        subtype=account.subtype,
                        amount=account.balances.current,
                        limit=account.balances.limit if account.balances.limit is not None else 0,
                        utilization=account.balances.current / account.balances.limit if account.balances.limit is not None else 0,
                        iso_currency_code=account.balances.iso_currency_code
                    ))
                elif _is_loan(account_type):
                    loan_liabilities.append(PlaidLoan(
                        account_id=account.account_id,
                        name=account.name,
                        mask=account.mask,
                        type=account.type,
                        subtype=account.subtype,
                        amount=account.balances.current,
                        iso_currency_code=account.balances.iso_currency_code
                    ))
            else:
                # Negative balances are overpaid credit cards
                if _is_credit_card(account_type, account_subtype):
                    credit_card_liabilities.append(PlaidCreditCard(
                        account_id=account.account_id,
                        name=account.name,
                        mask=account.mask,
                        amount=account.balances.current,
                        limit=account.balances.limit if account.balances.limit is not None else 0,
                        utilization=0
                    ))
    # Calculate totals
    total_credit_card = sum(liability.amount for liability in credit_card_liabilities)
    total_loan = sum(liability.amount for liability in loan_liabilities)
    total_liabilities = total_credit_card + total_loan
    
    return GetCurrentLiabilitiesResponse(
        credit_cards=CreditCardBreakdown(
            accounts=credit_card_liabilities,
            total=total_credit_card
        ),
        loans=LoanBreakdown(
            accounts=loan_liabilities,
            total=total_loan
        ),
        total_liabilities=total_liabilities
    )