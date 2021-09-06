from src.customer.schemas.get import responses
from .schemas import SearchCustomersQueryParams, SearchCustomersResponse


class Service:
    def get(
        self, query_params: SearchCustomersQueryParams
    ) -> list[SearchCustomersResponse]:
        data = [
            {
                "name": "elber",
                "last_name": "nava",
                "age": 15,
                "email": "dafd",
                "phone": "1234",
                "nationality": "us",
                "address": "aaa" "",
                "document_identification": "1234679800",
                "civl_status": "married",
            }
        ]
        response = []

        for elem in data:
            response.append(SearchCustomersResponse(**elem))

        return response
