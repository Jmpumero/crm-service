from typing import Any
from src.customer.repository import MongoQueries

from ..schemas import (
    CustomerProfileHeaderResponse,
)
from http_exceptions import NotFoundException


class ProfileHeaderService(MongoQueries):
    def __init__(self):
        super().__init__()

    async def get_profile_header(self, customer_id: str) -> Any:
        customer: Any = await self.customer.find_one({"_id": customer_id})

        if not customer:
            raise NotFoundException()

        languages = customer.get("language") or []

        data = {
            "_id": customer.get("_id", None),
            "name": customer.get("name", None),
            "image": "https://picsum.photos/200/300",
            "last_name": customer.get("last_name", None),
            "score": 0,
            "languages": [language.get("language", None) for language in languages],
            "country": customer.get("country", None),
            "membership": "?",
            "gender": "M",
            "age": customer.get("age", None),
            "next_hotel_stay": "random hotel",
            "next_stay_date": "25/10/2021",
            "last_checkout_date": "21/04/2021",
            "last_stay_hotel": "super random hotel",
            "total_stays": 1,
            "total_nights": 1,
            "days_since_last_stay": 15,
            "lifetime_expenses": 680.60,
            "total_lodging_expenses": 350.98,
            "miscellaneous_expenses": 329.62,
            "average_expenditure_per_stay": 680.60,
            "average_days_before_booking": 35,
        }

        return CustomerProfileHeaderResponse(**data)
