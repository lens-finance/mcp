# MCP tools package
from mcp_server.storage.item import item_storage

# Initialize the global item storage when the tools package is imported
# This ensures all tools have access to the same instance of ItemStorage
_storage = item_storage