from typing import Any
from pydantic.fields import T


from fastapi import status
from fastapi.responses import JSONResponse

from src.customer.repository import MongoQueries
from src.blacklist.repositories import BlacklistQueries

from src.blacklist.schemas import (
    BlacklistResponse,
    BlacklistUpdateResponse,
)


class BlacklistService(MongoQueries):
    def __init__(self):
        super().__init__()
        self.repository = BlacklistQueries()

    def build_blacklist_response(self, items) -> BlacklistResponse:
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
        return BlacklistResponse(**response)

    async def get_customers_blacklist(
        self, query, skip, limit, column_sort, order_sort, status
    ) -> BlacklistResponse:

        cursor = None
        items = None

        cursor = self.repository.blacklist_search(
            query, skip, limit, column_sort, order_sort, status
        )
        if cursor != None:
            items = await cursor.to_list(length=None)

        return self.build_blacklist_response(items)

    async def get_one_customer_bl(self, id_customer):
        ...

    async def update_(self, body) -> BlacklistUpdateResponse:
        resp = await self.repository.update_customer(body)

        if resp != None:

            response = {
                "code": 200,
                "message": f"Customer Update successfully ",
            }
        else:
            response = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": f"Customer don't Found",
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
        return response
