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

    def build_tab_profile_res(self, contact, interest, d_hotel):

        response = {}
        return {"contact": contact, "interest": interest, "data_hotel": d_hotel}

    async def get_profile_details(self, customer_id: str) -> Any:

        c_contact = await self.profile_detail.get_contact(customer_id)
        contact = await c_contact.to_list(length=None)
        interest = await self.get_interest_cast(customer_id)
        data_hotel = await self.profile_detail.get_data_tab_profile(customer_id)

        response = self.build_tab_profile_res(contact, interest, data_hotel)

        return response
