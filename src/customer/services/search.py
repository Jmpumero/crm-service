from pydantic.fields import T

from fastapi import status
from fastapi.responses import JSONResponse
from core.connection.connection import ConnectionMongo
from ..repositories import SearchQueries


class SearchService:
    def __init__(self):
        self.repository = SearchQueries()

    async def get_customers(self, skip, limit, q, order_sort, column_sort):
        # agregar lower case?
        cursor = self.repository.find_customers(
            skip, limit, order_sort.replace(" ", ""), column_sort.replace(" ", ""), q
        )
