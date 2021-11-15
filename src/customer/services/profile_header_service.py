import statistics
from datetime import datetime, timedelta
from functools import reduce
from typing import Any
from src.customer.repository import MongoQueries

from ..schemas import (
    CustomerProfileHeaderResponse,
)
from http_exceptions import NotFoundException

from src.customer.profile_sensors_endpoint.schemas.response.customers_sensors import (
    Forecasts,
    PmsGeneral,
)

from src.customer.profile_sensors_endpoint.repository.pms import PmsQueries
from src.customer.profile_sensors_endpoint.libs import pms_lib


class ProfileHeaderService(MongoQueries):
    def __init__(self):
        super().__init__()

    async def get_profile_header(self, customer_id: str) -> Any:
        revenue_list = []
        nights_list = []
        revenue_list = []
        anticipation_list = []
        stays_list = []

        customer: Any = await self.customer.find_one({"_id": customer_id})

        if not customer:
            raise NotFoundException()

        try:

            pms_queries = PmsQueries()

            # customer stays query
            customer_reservations_master = pms_queries.get_all_customer_stays(
                customer_id
            )

            # customer stays list
            reservations_list = [
                reservation async for reservation in customer_reservations_master
            ]

            for reservation in reservations_list:
                # nights
                if reservation["entity"] == "pms_booker":
                    for book in reservation["data"]["bBooks"]:
                        nights_list.append(book["nights"])
                else:
                    nights_list.append(reservation["data"]["nights"])

                # revenues
                async for revenue in pms_queries.get_upsellings_food_beverages(
                    customer_id, reservation["entity"]
                ):
                    revenue_list.append(revenue)

                # anticipation
                reservation_creation_date = datetime.strptime(
                    reservation["data"]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                reservation_checkin_date = datetime.strptime(
                    reservation["data"]["checkin"], "%Y-%m-%d"
                )
                anticipation_time = (
                    reservation_creation_date - reservation_checkin_date
                ) / timedelta(milliseconds=1)
                anticipation_list.append(anticipation_time)

                if reservation["entity"] == "pms_booker":
                    stays_list.append(
                        PmsGeneral(
                            last_property=reservation["data"]["sproperty"]["name"],
                            last_checkout=datetime.strptime(
                                reservation["data"]["bBooks"][-1]["checkout"],
                                "%Y-%m-%d",
                            ),
                        )
                    )
                else:
                    stays_list.append(
                        PmsGeneral(
                            last_property=reservation["data"]["riRatePlan"][
                                "sproperty"
                            ]["name"],
                            last_checkout=datetime.strptime(
                                reservation["data"]["checkout"],
                                "%Y-%m-%d",
                            ),
                        )
                    )

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

            lifetime_expenditure = (
                pms_lib.get_revenues(revenue_list_reduced, "ACCOMMODATION")["total"]
                + pms_lib.get_revenues(revenue_list_reduced, "UPSELLING")["total"]
                + pms_lib.get_revenues(revenue_list_reduced, "FOOD AND BEVERAGES")[
                    "total"
                ]
            )

            data = {
                "_id": customer.get("_id", None),
                "name": customer.get("name", None),
                "customer_avatar": customer.get("customer_avatar", None),
                "last_name": customer.get("last_name", None),
                # "score": 0,
                "languages": [language.get("language", None) for language in languages],
                "country": customer.get("country", None),
                # "membership": "?",
                "gender": customer.get("gender", None),
                "age": customer.get("age", None),
                # "next_hotel_stay": "random hotel",
                # "next_stay_date": "25/10/2021",
                "last_checkout_date": str(stays_list[-1].last_checkout.date()),
                "last_stay_hotel": stays_list[-1].last_property,
                "total_stays": len(reservations_list),
                "total_nights": reduce(lambda a, b: a + b, nights_list, 0),
                "days_since_last_stay": pms_lib.days_since_date(
                    stays_list[-1].last_checkout.date()
                ),
                "lifetime_expenses": lifetime_expenditure,
                "total_lodging_expenses": pms_lib.get_revenues(
                    revenue_list_reduced, "ACCOMMODATION"
                )["total"],
                "miscellaneous_expenses": pms_lib.get_revenues(
                    revenue_list_reduced, "UPSELLING"
                )["total"]
                + pms_lib.get_revenues(revenue_list_reduced, "FOOD AND BEVERAGES")[
                    "total"
                ],
                "average_expenditure_per_stay": lifetime_expenditure
                / len(reservations_list),
                "average_days_before_booking": int(statistics.mean(anticipation_list)),
            }

            return CustomerProfileHeaderResponse(**data)
        except Exception:
            data = {
                "_id": customer.get("_id", None),
                "name": customer.get("name", None),
                "customer_avatar": customer.get("customer_avatar", None),
                "last_name": customer.get("last_name", None),
                "languages": [language.get("language", None) for language in languages],
                "country": customer.get("country", None),
                "gender": customer.get("gender", None),
                "age": customer.get("age", None),
            }
            return CustomerProfileHeaderResponse(**data)
