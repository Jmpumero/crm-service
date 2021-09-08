from .repository import MongoQueries

from src.customer.schemas.get import responses
from .schemas import SearchCustomersQueryParams, SearchCustomersResponse


class Service(MongoQueries):
    def __init__(self) -> None:
        super().__init__()

    async def get_customers(
        self, skip, limit, query_params: SearchCustomersQueryParams
    ) -> list[SearchCustomersResponse]:

        customers = []

        total_customer = await self.total_customer()
        print(total_customer)
        if query_params.query == "":

            cursor = self.find_all_customers(skip, limit)

            for customer in await cursor.to_list(length=None):

                customers.append(SearchCustomersResponse(**customer))

        else:
            pass

        # for elem in data:
        #     response.append(SearchCustomersResponse(**elem))

        response = self.build_response(customers, total_customer)

        return response

    def build_response(self, list_customer, total_customer):

        pass
