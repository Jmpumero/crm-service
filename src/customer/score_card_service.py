from typing import Any


class ScoreCardService:
    async def get_customer_score_card(self, customer_id: str):
        data = [
            {
                "name": "purchase_recurrence",
                "data": {
                    "range": {"min": 0, "max": 25},
                    "score": 25,
                    "date_range": {"min": "07/08/2021", "max": "27/09/2021"},
                },
            },
            {
                "name": "room_reservations",
                "data": [
                    {"room_type": {"type": "basic", "score": 25}},
                    {
                        "contracted_rate_per_night": {
                            "range": {"min": 0, "max": 25},
                            "score": 25,
                        }
                    },
                    {"number_of_nights": {"range": {"min": 0, "max": 25}, "score": 25}},
                    {
                        "booking_anticipation": {
                            "range": {"min": 0, "max": 25},
                            "score": 25,
                        }
                    },
                    {
                        "contracted_cancellation_policy": {
                            "type": "basic",
                            "score": 25,
                        },
                    },
                    {
                        "meal_plan_contracted": {"type": "basic", "score": 25},
                    },
                ],
            },
            {
                "name": "purchase_of_extra_services",
                "data": [
                    {"service_type": {"type": "basic", "socore": 25}},
                    {
                        "amount_of_upsellings_contracted": {
                            "range": {"min": 25, "max": 25},
                            "score": 25,
                        }
                    },
                    {
                        "number_of_upsellings_purchased": {
                            "range": {"min": 25, "max": 25},
                            "score": 25,
                        },
                    },
                    {
                        "number_of_cross_sellings_purchased": {
                            "range": {"min": 25, "max": 25},
                            "score": 25,
                        }
                    },
                    {
                        "amount_of_upsellings_purchased": {
                            "range": {"min": 25, "max": 25},
                            "score": 25,
                        }
                    },
                ],
            },
            {
                "name": "purchase_in_the_restaurant",
                "data": [
                    {
                        "product_category": {"type": "basic", "socore": 25},
                        "average_restaurant_ticket": {
                            "range": {
                                "min": 25,
                                "max": 25,
                            },
                            "score": 25,
                        },
                        "time_spent_at_the_table": {
                            "range": {
                                "min": 25,
                                "max": 25,
                            },
                            "score": 25,
                        },
                        "booking_anticipation": {
                            "range": {
                                "min": 25,
                                "max": 25,
                            },
                            "score": 25,
                        },
                    }
                ],
            },
        ]

        return data

    async def put_score_card(self, customer_id: str, data: Any):
        print(data.dict())

        return "fino señores"
