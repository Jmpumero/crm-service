from .repository import MongoQueries

from src.customer.schemas.get import responses
from .schemas import SearchCustomersQueryParams, SearchCustomersResponse


class Service(MongoQueries):
    def __init__(self) -> None:
        super().__init__()

    def get_customers(
        self, skip, limit, query_params: SearchCustomersQueryParams
    ) -> list[SearchCustomersResponse]:

        print(query_params.column_name)

        if query_params.query is "":

            print("gege")
        else:
            pass
        response = []

        # for elem in data:
        #      response.append(SearchCustomersResponse(**elem))

        return response
