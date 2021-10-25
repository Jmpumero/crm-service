import json
from typing import Any

from aioredis.client import Redis

from src.customer.repository import MongoQueries


class SalesSummary(MongoQueries):
    def __init__(self):
        super().__init__()

    async def get_customer_sales_summary(self, customer_id: str, redis: Redis) -> Any:
        customer_in_redis: str = await redis.get(str(customer_id))

        if customer_in_redis:
            return json.loads(customer_in_redis)

        data: Any = {
            "total_revenue": [
                {"name": "upgrade_and_upselling", "quantity": 110},
                {"name": "food_and_beverage", "quantity": 150},
                {"name": "lodging", "quantity": 130},
            ],
            "frequent_visits": [
                {"name": "superior king", "quantity": 4},
                {"name": "king", "quantity": 2},
                {"name": "double", "quantity": 2},
            ],
            "most_contracted_services": [
                {"name": "extra key", "quantity": 118},
                {"name": "tablet rental", "quantity": 112},
                {"name": "spa access", "quantity": 220},
                {"name": "bottle of wine", "quantity": 80},
            ],
            "checks_in": [
                {"name": "complete", "quantity": 8},
                {"name": "no complete", "quantity": 2},
            ],
            "most_visited_pages": await self.get_most_visited_pages(customer_id),
            "use_of_suite_applications": [],
            "frequency_of_use_of_suite_applications": [
                {"name": "cast", "quantity": 7},
                {"name": "hostpod", "quantity": 11},
            ],
            "segment_where_it_is_located": [],
        }

        await redis.set(str(customer_id), json.dumps(data), ex=120)

        return data

    async def get_most_visited_pages(self, customer_id: str) -> Any:
        cursor: Any = self.cast_collection.find({"customer_id": customer_id})

        customers: Any = await cursor.to_list(None)

        most_visited_pages = {}

        for customer in customers:
            most_visited_pages[
                customer.get("data").get("playback_pair").get("appName")
            ] = (
                most_visited_pages.get(
                    customer.get("data").get("playback_pair").get("appName"), 0
                )
                + 1
            )

        most_visited_pages: Any = [
            {"name": page[0], "quantity": page[1]}
            for page in sorted(
                most_visited_pages.items(), key=lambda x: x[1], reverse=True
            )
        ]

        return most_visited_pages[:5]
