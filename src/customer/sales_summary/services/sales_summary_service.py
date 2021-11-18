from typing import Any, Optional
from functools import reduce

from fastapi import status
from fastapi.responses import JSONResponse

from src.customer.sales_summary.repository.sales_summary_queries import (
    SalesSummaryQueries,
)

from core.libs import pms_lib

from src.customer.sales_summary.schemas.response.sales_summary_response import (
    Forecasts,
    MostVisitedApps,
    FrequentRooms,
)


class SalesSummaryService(SalesSummaryQueries):
    """
    Service to get PMS usage statistics

    """

    def __init__(self):
        super().__init__()

    async def __most_used_room_types(self, customer_id):

        rooms_booker = await self.group_by_most_used_roomType(
            customer_id, "pms_booker"
        ).to_list(None)

        rooms_guest = await self.group_by_most_used_roomType(
            customer_id, "pms_pri_guest"
        ).to_list(None)

        rooms_types = rooms_booker + rooms_guest

        room_type_list = [
            FrequentRooms(room_name=app["_id"][0], count=app["count"])
            if app["_id"]
            else FrequentRooms(room_name="Not Defined", count=app["count"])
            for app in rooms_types
        ]

        return room_type_list

    async def __get_most_used_apps(self, customer_id):
        playback_used_apps_list = []
        most_used_app = self.group_by_most_used_app(customer_id)

        playback_used_apps_list = [
            MostVisitedApps(app_name=app["_id"], visit_count=app["count"])
            async for app in most_used_app
        ]

        return playback_used_apps_list

    async def __get_completed_checkins(self, customer_id):
        """Cancellation Percentage"""

        cancellations_booker = await self.get_cancellations(
            customer_id, "pms_booker"
        ).to_list(None)

        cancellations_guest = await self.get_cancellations(
            customer_id, "pms_pri_guest"
        ).to_list(None)

        total_cancellations = cancellations_booker + cancellations_guest

        completed = [
            i["count"]
            for i in total_cancellations
            if (i["_id"] == ["hosted"]) or (i["_id"] == ["checkout"])
        ]

        non_completed = [
            i["count"]
            for i in total_cancellations
            if (i["_id"] != ["hosted"]) or (i["_id"] != ["checkout"])
        ]

        return {
            "completed": reduce(lambda a, b: a + b, completed, 0),
            "non_completed": reduce(lambda a, b: a + b, non_completed, 0),
        }

    async def __total_revenue(self, customer_id):
        """Graph for extras over revenue income percentage"""

        revenues_booker = await self.get_upsellings_food_beverages(
            customer_id, "pms_booker"
        ).to_list(None)

        revenues_guest = await self.get_upsellings_food_beverages(
            customer_id, "pms_pri_guest"
        ).to_list(None)

        joined_list = revenues_booker + revenues_guest

        revenues_list = [
            Forecasts(
                concept=item["_id"],
                count=item["count"],
                net_amount=item["total_income"],
                avg_income=item["average_income"],
            )
            for item in joined_list
        ]

        revenue_list_reduced = [i.dict() for i in revenues_list]

        upsellings = pms_lib.get_revenues(revenue_list_reduced, "UPSELLING")["total"]
        food_beverages = pms_lib.get_revenues(
            revenue_list_reduced, "FOOD AND BEVERAGES"
        )["total"]
        accomodation = pms_lib.get_revenues(revenue_list_reduced, "ACCOMMODATION")[
            "total"
        ]

        return {
            "upsellings": upsellings,
            "food_beverages": food_beverages,
            "accomodation": accomodation,
        }

    async def get_sales_summary_graphs(self, customer_id):
        response = {
            "total_revenue": await self.__total_revenue(customer_id),
            "frequent_rooms": await self.__most_used_room_types(customer_id),
            "most_contracted_services": None,
            "average_checkins": await self.__get_completed_checkins(customer_id),
            "most_visited_apps": await self.__get_most_used_apps(customer_id),
            "app_suite_usage": None,
            "app_frequency": None,
            "segment": None,
        }

        return response
