from datetime import date

from pydantic import BaseModel

class PlaidConnection(BaseModel):
    name: str
    access_token: str
    item_id: str

class DateRange(BaseModel):
    start_date: date
    end_date: date

