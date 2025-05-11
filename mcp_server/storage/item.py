from mcp_server.utils import read_access_tokens
from mcp_server.tools.schemas.util import PlaidConnection
from typing import Any, Optional


class ItemStorage:
    _instance: Optional["ItemStorage"] = None
    items: dict[str, PlaidConnection] = {}
    accounts: dict[str, list[dict[str, Any]]] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ItemStorage, cls).__new__(cls)
            cls._instance.items = read_access_tokens()
        return cls._instance

    def get_item(self, name: str) -> PlaidConnection:
        if not name in self.items:
            self.items = read_access_tokens()

        return self.items[name]
    
    def get_items(self) -> dict[str, PlaidConnection]:
        return self.items

    def add_item(self, name: str, item: PlaidConnection):
        self.items[name] = item

    def delete_item(self, name: str):
        del self.items[name]


# Global instance that can be imported anywhere
item_storage = ItemStorage()