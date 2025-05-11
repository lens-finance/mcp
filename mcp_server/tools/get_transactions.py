from datetime import datetime
from mcp_server.services.plaid.client import plaid_client
from mcp_server.tools.constants import DEFAULT_DATE_RANGE
from mcp_server.tools.get_accounts import get_all_items
from mcp_server.enums.plaid import PlaidAccountType
from plaid.model.transactions_get_request import TransactionsGetRequest
from plaid.model.transactions_get_request_options import TransactionsGetRequestOptions
from collections import defaultdict

from mcp_server.tools.schemas.io import AccountBreakdown, CategoryBreakdown, GetAllTransactionsResponse, SummarizeTransactionsResponse
from mcp_server.tools.schemas.tools import PlaidAccount, PlaidCategory, PlaidTransaction
from mcp_server.tools.schemas.util import DateRange

def get_transactions(
    start_date: str = DEFAULT_DATE_RANGE.start_date.isoformat(),
    end_date: str = DEFAULT_DATE_RANGE.end_date.isoformat(),
    account_type: PlaidAccountType | None = None,
) -> SummarizeTransactionsResponse:
    all_transactions = get_all_transactions(start_date, end_date, account_type)
    return summarize_transactions(all_transactions)

def get_all_transactions(
    start_date: str = DEFAULT_DATE_RANGE.start_date.isoformat(),
    end_date: str = DEFAULT_DATE_RANGE.end_date.isoformat(),
    account_type: PlaidAccountType | None = None,
) -> GetAllTransactionsResponse:
    """
    Retrieves transaction data for specified accounts within a date range.
    
    Args:
        start_date: Start date for transactions in ISO format (YYYY-MM-DD)
        end_date: End date for transactions in ISO format (YYYY-MM-DD)
        account_type: Optional account type to filter by
        
    Returns:
        A dictionary containing transaction data for the requested accounts
    """
    accounts: list[PlaidAccount] = []
    account_to_token_map: dict[str, str] = {}
    items = get_all_items() 
    for item in items:
        for account in item.accounts:
            if not account_type or account.type == account_type:
                accounts.append(account)
                account_to_token_map[account.account_id] = item.access_token
    if not accounts:
        return GetAllTransactionsResponse(
            transactions=[],
            total_transactions=0,
            total_amount=0
        )
    
    # Get all transactions for each account
    all_transactions: list[PlaidTransaction] = []
    for account in accounts:
        access_token = account_to_token_map[account.account_id]

        # Create request options with account filter
        options = TransactionsGetRequestOptions(
            account_ids=[account.account_id]
        )

        # Create and send request to Plaid API
        request = TransactionsGetRequest(
            access_token=access_token,
            start_date=datetime.strptime(start_date, "%Y-%m-%d").date(),
            end_date=datetime.strptime(end_date, "%Y-%m-%d").date(),
            options=options
        )
        
        response = plaid_client.client.transactions_get(request)
        transactions = response.to_dict()["transactions"]
        
        # Add account info to each transaction
        for transaction in transactions:
            txn = PlaidTransaction(
                account_id=transaction["account_id"],
                amount=transaction["amount"],
                authorized_date=transaction["authorized_date"],
                authorized_datetime=transaction["authorized_datetime"],
                iso_currency_code=transaction["iso_currency_code"],
                merchant_name=transaction["merchant_name"],
                name=transaction["name"],
                txn_date=transaction["date"],
                txn_datetime=transaction["datetime"],
                pending=transaction["pending"],
                category=transaction["personal_finance_category"],
                website=transaction["website"],
                account_name=account.name,
                account_type=account.type,
                account_subtype=account.subtype,
            )

            all_transactions.append(txn)
        
            
    
    all_transactions.sort(key=lambda x: x.txn_date, reverse=True)    
    total_amount = round(sum(tx.amount for tx in all_transactions), 2)

    if len(all_transactions) > 20:
        all_transactions = [tx.to_compact() for tx in all_transactions]
    
    return GetAllTransactionsResponse(
        transactions=all_transactions,
        total_transactions=len(all_transactions),
        total_amount=total_amount
    )
    
    

def summarize_transactions(transactions_response: GetAllTransactionsResponse) -> SummarizeTransactionsResponse:
    """
    Creates a summary of transaction data including breakdowns by account and category.
    
    Args:
        transactions_response: Response dictionary from get_transactions()
        
    Returns:
        A dictionary containing summary statistics and breakdowns
    """
    transactions = transactions_response.transactions
    
    # Initialize summary data structures
    account_totals = defaultdict(float)
    account_counts = defaultdict(int)
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    
    # Calculate date range
    dates = [tx.txn_date for tx in transactions]
    date_range = DateRange(
        start_date=min(dates),
        end_date=max(dates)
    ) if dates else None
    
    # Calculate summaries
    for transaction in transactions:
        amount = transaction.amount
        account_name = transaction.account_name
        category = transaction.category or PlaidCategory(
            primary="Uncategorized",
            detailed="Uncategorized",
            confidence_level="LOW"
        )
        
        account_totals[account_name] += amount
        account_counts[account_name] += 1
        category_totals[category.primary] += amount
        category_counts[category.primary] += 1
    
    # Format account breakdown
    account_breakdown = [
        AccountBreakdown(
            account_name=account,
            total_amount=round(total, 2),
            transaction_count=account_counts[account],
            average_transaction=round(total / account_counts[account], 2)
        )
        for account, total in account_totals.items()
    ]
    
    # Format category breakdown
    category_breakdown = [
        CategoryBreakdown(
            category=category,
            total_amount=round(total, 2),
            transaction_count=category_counts[category],
            average_transaction=round(total / category_counts[category], 2)
        )
        for category, total in category_totals.items()
    ]
    
    # Sort breakdowns by total amount
    account_breakdown.sort(key=lambda x: x.total_amount, reverse=True)
    category_breakdown.sort(key=lambda x: x.total_amount, reverse=True)
    
    return SummarizeTransactionsResponse(
        date_range=date_range,
        total_amount=transactions_response.total_amount,
        total_transactions=transactions_response.total_transactions,
        average_transaction_amount=round(transactions_response.total_amount / transactions_response.total_transactions, 2) if transactions_response.total_transactions > 0 else 0,
        account_breakdown=account_breakdown,
        category_breakdown=category_breakdown
    )
    