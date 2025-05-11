from collections import defaultdict

from mcp_server.tools.get_transactions import get_all_transactions
from mcp_server.tools.schemas.tools import PlaidTransaction
from mcp_server.tools.schemas.io import CategorizedSummary, CategorySummary 
from mcp_server.tools.schemas.util import DateRange

def get_categorized_summary(
    start_date: str,
    end_date: str,
) -> CategorizedSummary:
    """
    Get a categorized summary of transactions within a date range.
    
    Args:
        start_date: Start date in ISO format (YYYY-MM-DD)
        end_date: End date in ISO format (YYYY-MM-DD)
        
    Returns:
        CategorizedSummary object containing transaction summaries by category
    """
    # Get all transactions
    transactions_response = get_all_transactions(start_date=start_date, end_date=end_date)
    transactions = transactions_response.transactions
    
    # Initialize category dictionaries
    category_transactions = defaultdict(list[PlaidTransaction])
    category_totals = defaultdict(float)
    category_counts = defaultdict(int)
    
    # Process each transaction
    for txn in transactions:
        # Use personal finance category if available, otherwise use merchant name
        category = txn.category.primary if txn.category else "Uncategorized"
        
        # Add transaction to category
        category_transactions[category].append(txn)
        
        # Update category totals
        category_totals[category] += txn.amount
        category_counts[category] += 1
    
    # Create category summaries
    category_summaries = {}
    for category, transactions_in_category in category_transactions.items():
        # Sort transactions by date (most recent first)
        sorted_transactions = sorted(transactions_in_category, key=lambda x: x.txn_date, reverse=True)
        
        # Create category summary
        category_summaries[category] = CategorySummary(
            total_amount=round(category_totals[category], 2),
            transaction_count=category_counts[category],
            average_transaction=round(category_totals[category] / category_counts[category], 2),
            transactions=sorted_transactions
        )
    
    # Create date range
    date_range = DateRange(
        start_date=min(txn.txn_date for txn in transactions) if transactions else start_date,
        end_date=max(txn.txn_date for txn in transactions) if transactions else end_date
    )
    
    # Create and return final summary
    return CategorizedSummary(
        categories=category_summaries,
        total_transactions=len(transactions),
        total_amount=round(sum(txn.amount for txn in transactions), 2),
        date_range=date_range
    )
