from mcp_server.tools.constants import DEFAULT_DATE_RANGE
from mcp_server.tools.get_transactions import get_all_transactions
from mcp_server.tools.schemas.io import GetAllTransactionsResponse

def get_transactions_by_vendor(
    vendor: str,
    start_date: str = DEFAULT_DATE_RANGE.start_date.strftime("%Y-%m-%d"),
    end_date: str = DEFAULT_DATE_RANGE.end_date.strftime("%Y-%m-%d"),
) -> GetAllTransactionsResponse:
    """
    Get all transactions by vendor

    Args:
        vendor: The vendor to filter by
        start_date: The start date to filter by (YYYY-MM-DD)
        end_date: The end date to filter by (YYYY-MM-DD)

    Returns:
        A list of transactions
    """
    all_transactions = get_all_transactions(
        start_date=start_date,
        end_date=end_date
    )

    cleaned_vendor = vendor.lower().strip()
    txn_vendor = lambda txn: txn.merchant_name.lower() if txn.merchant_name else txn.name.lower()

    filtered_transactions = [
        txn for txn in all_transactions.transactions
        if cleaned_vendor in txn_vendor(txn)
    ]

    return GetAllTransactionsResponse(
        transactions=filtered_transactions,
        total_transactions=len(filtered_transactions),
        total_amount=sum(txn.amount for txn in filtered_transactions)
    )
    

