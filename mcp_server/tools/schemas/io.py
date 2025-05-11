from pydantic import BaseModel

from mcp_server.tools.schemas.tools import CompactPlaidTransaction, PlaidAccount, PlaidCreditCard, PlaidLoan, PlaidTransaction
from mcp_server.tools.schemas.util import DateRange

class GetAllTransactionsResponse(BaseModel):
    transactions: list[CompactPlaidTransaction]
    total_transactions: int
    total_amount: float

class AccountBreakdown(BaseModel):
    account_name: str
    total_amount: float
    transaction_count: int
    average_transaction: float

class CategoryBreakdown(BaseModel):
    category: str
    total_amount: float
    transaction_count: int
    average_transaction: float

class SummarizeTransactionsResponse(BaseModel):
    date_range: DateRange | None
    total_transactions: int
    total_amount: float
    average_transaction_amount: float
    account_breakdown: list[AccountBreakdown]
    category_breakdown: list[CategoryBreakdown]


class CreditCardBreakdown(BaseModel):
    accounts: list[PlaidCreditCard]
    total: float

class LoanBreakdown(BaseModel):
    accounts: list[PlaidLoan]
    total: float

class GetCurrentLiabilitiesResponse(BaseModel):
    credit_cards: CreditCardBreakdown
    loans: LoanBreakdown
    total_liabilities: float

class NetWorthAssetBreakdown(BaseModel):
    accounts: list[PlaidAccount]
    total: float

class NetWorthLiabilityBreakdown(BaseModel):
    accounts: list[PlaidAccount]
    total: float

class GetNetWorthResponse(BaseModel):
    assets: NetWorthAssetBreakdown
    liabilities: NetWorthLiabilityBreakdown
    net_worth: float

class CategoryTaxonomy(BaseModel):
    primary_category: str
    sub_category: str 
    description: str

class CategorySummary(BaseModel):
    total_amount: float
    transaction_count: int
    average_transaction: float
    transactions: list[CompactPlaidTransaction]

class CategorizedSummary(BaseModel):
    categories: dict[str, CategorySummary]
    total_transactions: int
    total_amount: float
    date_range: DateRange