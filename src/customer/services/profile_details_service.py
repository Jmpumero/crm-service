from typing import Any
from src.customer.repository import MongoQueries
from ..schemas import CustomerProfileDetailResponse


class ProfileDetailService(MongoQueries):
    def __init__(self):
        super().__init__()

    async def get_profile_details(self, customer_id: str) -> Any:
        customer = await self.customer.find_one({"_id": customer_id})

        if not customer:
            return {}

        customer_phones = customer.get("phone") or []

        data = {
            "most_visited_hotel": "random hotel",
            "recency": 0,
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
                "hotspot": {"ads_viewed": 16},
                "sms": {"sent_sms": 514},
                "signage": {"ads_sent": 100, "used_devices": 4},
                "butler": {"ads_sent": 16},
            },
        }

        return CustomerProfileDetailResponse(**data)

    async def get_contact_modal_info(self, customer_id: str):
        customer = await self.customer.find_one({"_id": customer_id})

        if not customer:
            return {}

        emails = customer.get("email")
        phones = customer.get("phone")
        addresses = customer.get("address")
        social_medias = customer.get("social_media")

        return {
            "emails": emails,
            "phones": phones,
            "addresses": addresses,
            "social_medias": social_medias,
        }
