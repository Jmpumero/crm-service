from typing import Any
from src.customer.repository import MongoQueries
from ..schemas import CustomerProfileDetailResponse


class ProfileDetailService(MongoQueries):
    async def get_profile_details(self, customer_id: str) -> Any:
        customer = await self.customer.find_one({"_id": customer_id})

        if not customer:
            return {}

        customer_phones = customer.get("phone") or []

        data = {
            "most_visited_hotel": "random hotel",
            "recency": "?",
            "email": [emailDict["email"] for emailDict in customer.get("email")],
            "phone": [customerDict["intl_format"] for customerDict in customer_phones],
            "social_networks": [
                {"name": "Instagram", "username": "@randomuser"},
                {"name": "Facebook", "username": "@randomuserfacebook"},
            ],
            "accepted_terms": [
                {
                    "document_url": "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
                    "name": "Terminos 2021",
                    "description": "Terminos actualizados sobre el uso de nuestros servicios",
                }
            ],
            "interests": ["Basketball", "Chess", "CSGO"],
            "communication_methods": {
                "email": {"sent": 125, "opened": 15},
                "hostpod": {"ads_viewed": 16},
                "sms": {"sent_sms": 514},
                "signage": {"ads_sent": 100, "used_devices": 4},
                "butler": {"ads_sent": 16},
            },
        }

        return CustomerProfileDetailResponse(**data)
