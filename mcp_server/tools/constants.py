
from datetime import date, timedelta
from mcp_server.tools.schemas.util import DateRange


DEFAULT_DATE_RANGE = DateRange(
    start_date=date.today() - timedelta(days=14),
    end_date=date.today()
)