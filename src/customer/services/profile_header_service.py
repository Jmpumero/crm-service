from functools import reduce
from typing import Any
from src.customer.repository import MongoQueries

from ..schemas import (
    CustomerProfileHeaderResponse,
)
from http_exceptions import NotFoundException

from src.customer.profile_sensors_endpoint.schemas.response.customers_sensors import (
    PmsBook,
    PmsHistoryPrimaryGuest,
    PmsHistorySecondaryGuest,
    PmsGeneral,
    Forecasts,
)

from src.customer.profile_sensors_endpoint.repository.pms import PmsQueries
from src.customer.profile_sensors_endpoint.libs import pms_lib


class ProfileHeaderService(MongoQueries):
    def __init__(self):
        super().__init__()

    async def get_profile_header(self, customer_id: str) -> Any:
        revenue_list = []

        customer: Any = await self.customer.find_one({"_id": customer_id})

        if not customer:
            raise NotFoundException()

        pms_queries = PmsQueries()

        # customer stays query
        customer_reservations_master = pms_queries.get_all_customer_stays(customer_id)

        # customer stays list
        reservations_list = [
            reservation async for reservation in customer_reservations_master
        ]

        # custromer total nights
        nights = [
            [reservation["nights"] for reservation in reservation["data"]["bBooks"]]
            for reservation in reservations_list
        ]

        flatten_nights = [val for sublist in nights for val in sublist]

        # revenues
        async for reserv in customer_reservations_master:

            revenue_list = [
                revenue
                async for revenue in pms_queries.get_upsellings_food_beverages(
                    customer_id, reserv["entity"]
                )
            ]

        revenue_clean = pms_lib.remove_duplicates(revenue_list)

        forecasts_list = [
            Forecasts(
                concept=item["_id"],
                count=item["count"],
                net_amount=item["total_income"],
                avg_income=item["average_income"],
            )
            for item in revenue_clean
        ]

        revenue_list_reduced = [i.dict() for i in forecasts_list]

        languages = customer.get("language") or []

        data = {
            "_id": customer.get("_id", None),
            "name": customer.get("name", None),
            "image": customer.get("customer_avatar", None),
            "last_name": customer.get("last_name", None),
            # "score": 0,
            "languages": [language.get("language", None) for language in languages],
            "country": customer.get("country", None),
            # "membership": "?",
            "gender": customer.get("gender", None),
            "age": customer.get("age", None),
            # "next_hotel_stay": "random hotel",
            # "next_stay_date": "25/10/2021",
            "last_checkout_date": "21/04/2021",
            "last_stay_hotel": "super random hotel",
            "total_stays": await pms_queries.count_customer_master_books(customer_id),
            "total_nights": reduce(lambda a, b: a + b, flatten_nights, 0),
            "days_since_last_stay": 15,
            "lifetime_expenses": 0,
            "total_lodging_expenses": pms_lib.get_revenues(
                revenue_list_reduced, "ACCOMMODATION"
            )["total"],
            "miscellaneous_expenses": pms_lib.get_revenues(
                revenue_list_reduced, "UPSELLING"
            )["total"]
            + pms_lib.get_revenues(revenue_list_reduced, "FOOD AND BEVERAGES")["total"],
            "average_expenditure_per_stay": 680.60,
            "average_days_before_booking": 35,
        }

        return CustomerProfileHeaderResponse(**data)
