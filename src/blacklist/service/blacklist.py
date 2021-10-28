from typing import Any

from pydantic.fields import T

from src.customer.repository import MongoQueries
from src.blacklist.repositories import BlacklistQueries

from src.blacklist.schemas import (
    BlacklistCustomersResponse,
    BlacklistCustomer,
    BlacklistQueryParams,
)


class BlacklistService(MongoQueries):
    def __init__(self):
        super().__init__()
        self.repository = BlacklistQueries()

    def build_blacklist_response(self, items):
        if len(items[0]["items"]) > 0:
            response = {
                "total_items": items[0]["total_items"][0]["total"],
                "total_show": items[0]["total_show"][0]["total_show"],
                "items": items[0]["items"],
            }
        else:
            response = {
                "total_items": 0,
                "total_show": 0,
                "items": items[0]["items"],
            }
        return response

    async def get_customers_blacklist(self, query_params: BlacklistQueryParams) -> Any:

        cursor = None
        items = None

        cursor = self.repository.blacklist_search(query_params)
        if cursor != None:
            items = await cursor.to_list(length=None)

        return self.build_blacklist_response(items)

    # async def post_blacklist_update_customer(self, body: BlackListBody):

    #     return await self.update_customer_in_blacklist(body)
