from fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

# Import tools explicitly
from mcp_server.tools.get_accounts import get_all_items, get_item_by_name
from mcp_server.tools.get_transactions import get_all_transactions, get_transactions
from mcp_server.tools.get_net_worth import get_net_worth
from mcp_server.tools.get_current_liabilities import get_current_liabilities
from mcp_server.tools.get_category_taxonomy import get_category_taxonomy
from mcp_server.tools.get_categorized_summary import get_categorized_summary
from mcp_server.tools.get_filtered_transactions import get_transactions_by_vendor

app = FastMCP(name="TTYF MCP Server")

# Register tools with FastMCP
app.add_tool(get_all_items)
app.add_tool(get_item_by_name)
app.add_tool(get_transactions)
app.add_tool(get_all_transactions)
app.add_tool(get_net_worth)
app.add_tool(get_current_liabilities)
app.add_tool(get_category_taxonomy)
app.add_tool(get_categorized_summary)
app.add_tool(get_transactions_by_vendor)