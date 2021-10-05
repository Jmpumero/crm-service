from typing import Any

from src.customer.repository import MongoQueries
from ..schemas import CustomerMarketingSubscriptions


class MarketingSubscriptionsService(MongoQueries):
    async def get_customer_marketing_subscriptions(self, customer_id: str) -> Any:
        customer = await self.clients_customer.find_one({"_id": customer_id})

        emails = [
            {
                "email": customer_email.get("email"),
                "subscribed": customer_email.get("subscribed", False),
                "is_primary": customer_email.get("isMain", False),
            }
            for customer_email in customer["email"]
        ]

        phones = [
            {
                "phone": customer_phone.get("intl_format"),
                "is_primary": customer_phone.get("isMain", False),
                "subscribed": customer_phone.get("subscribed", False),
            }
            for customer_phone in customer.get("phone")
        ]

        data = {
            "emails": emails,
            "devices": [
                {
                    "mac_address": "00:00:00:00:00:01",
                    "subscribed": False,
                },
                {
                    "mac_address": "00:00:00:00:00:02",
                    "subscribed": True,
                },
            ],
            "phones": phones,
        }

        return CustomerMarketingSubscriptions(**data)
