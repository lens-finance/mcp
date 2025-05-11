from enum import Enum


class PlaidAccountType(str, Enum):
    CREDIT = "credit"
    DEPOSITORY = "depository"
    INVESTMENT = "investment"
    LOAN = "loan"
    OTHER = "other"

class PlaidAccountSubtype(str, Enum):
    CHECKING = "checking"
    SAVINGS = "savings"
    MONEY_MARKET = "money market"
    CREDIT_CARD = "credit card"
    CD = "cd"
    TFSA = "tfsa"
    RRSP = "rrsp"
    STUDENT = "student"
    MORTGAGE = "mortgage"
    AUTO = "hsa"
    HOME = "cash management"
    PERSONAL = "credit card"