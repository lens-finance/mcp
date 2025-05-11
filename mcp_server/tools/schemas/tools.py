from datetime import datetime, date
from pydantic import BaseModel

class PlaidBalance(BaseModel):
    available: float | None = None
    current: float | None = None
    iso_currency_code: str | None = None
    limit: float | None = None

class PlaidAccount(BaseModel):
    account_id: str
    balances: PlaidBalance
    mask: str
    name: str
    holder_category: str | None = None
    official_name: str | None = None
    subtype: str
    type: str

class PlaidItem(BaseModel):
    name: str
    accounts: list[PlaidAccount]
    item_id: str | None = None
    access_token: str | None = None

class PlaidTransactionCounterparty(BaseModel):
    name: str
    type: str
    website: str | None = None
    logo_url: str | None = None
    entity_id: str | None = None
    confidence_level: str | None = None

class PlaidCategory(BaseModel):
    confidence_level: str
    detailed: str
    primary: str

class CompactPlaidTransaction(BaseModel):
    amount: float
    merchant_name: str | None = None
    name: str
    txn_date: date
    category: PlaidCategory | None = None



class PlaidTransaction(CompactPlaidTransaction):
    account_id: str
    iso_currency_code: str
    pending: bool
    authorized_date: date | None = None
    authorized_datetime: datetime | None = None
    txn_datetime: datetime | None = None

    website: str | None = None
    account_name: str | None = None
    account_type: str | None = None
    account_subtype: str | None = None

    def to_compact(self) -> CompactPlaidTransaction:
        return CompactPlaidTransaction(
            amount=self.amount,
            merchant_name=self.merchant_name,
            name=self.name,
            txn_date=self.txn_date,
            category=self.category
        )

class PlaidLiability(BaseModel):
    account_id: str
    name: str
    mask: str
    amount: float
    type: str
    subtype: str
    iso_currency_code: str
    official_name: str | None = None

class PlaidCreditCard(PlaidLiability):
    limit: float
    utilization: float

class PlaidLoan(PlaidLiability):
    ...


