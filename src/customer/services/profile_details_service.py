from typing import Any

from src.customer.repository import MongoQueries
from ..schemas import CustomerProfileDetailResponse
from http_exceptions import NotFoundException
from ..repositories import PDQueries

from ..sales_summary import SalesSummaryQueries


class ProfileDetailService(MongoQueries):
    def __init__(self):
        super().__init__()
        self.profile_detail = PDQueries()
        self.sales_summary = SalesSummaryQueries()

    async def get_interest_cast(self, customer_id):
        c_interest = self.sales_summary.group_by_most_used_app(customer_id)
        r = await c_interest.to_list(length=None)
        a_interest = []
        for item in r:
            a_interest.append(item["_id"])

        return a_interest

    async def get_profile_details(self, customer_id: str) -> Any:

        c_contact = await self.profile_detail.get_contact(customer_id)
        interest = await self.get_interest_cast(customer_id)

        a = await self.profile_detail.get_most_visited_hotel(customer_id)

        return a
