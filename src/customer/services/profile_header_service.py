from typing import Any
from src.customer.repository import MongoQueries

from ..schemas import (
    CustomerProfileHeaderResponse,
)


class ProfileHeaderService(MongoQueries):
    async def get_profile_header(self, customer_id: str) -> Any:
        customer = await self.clients_customer.find_one({"_id": customer_id})

        if not customer:
            return {}

        data = {
            "_id": customer.get("_id", None),
            "name": customer.get("name", None),
            "score": 50,
            "languages": [language["language"] for language in customer["language"]],
            "country": customer.get("country", None),
            "membership": "?",
            "gender": "NO BINARY KEK",
            "age": customer.get("age", None),
            "next_hotel_stay": "random hotel",
            "next_stay_date": "25/10/2021",
            "last_checkout_date": "21/04/2021",
            "last_stay_hotel": "super random hotel",
            "total_stays": 1,
            "days_since_last_stay": 15,
            "lifetime_expenses": 680.60,
            "total_lodging_expenses": 350.98,
            "miscellaneous_expenses": 329.62,
            "average_expenditure_per_stay": 680.60,
            "average_days_before_booking": 35,
        }

        return CustomerProfileHeaderResponse(**data)
