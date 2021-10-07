from typing import Any

import bson

from .repository import MongoQueries
from fastapi import HTTPException

"""
example model of score:

[
    {
        "name": "purchase_recurrence",
        "data": [
            {
                "range": {
                    "min": 0,
                    "max": 25
                },
                "score": 25
            }
        ],
        "date_range": {
            "min": "07/08/2021",
            "max": "27/09/2021"
        }
    },
    {
        "name": "room_reservations",
        "data": [
            {
                "name": "room_type",
                "data": [
                    {
                        "type": "basic",
                        "score": 25
                    }
                ]
            },
            {
                "name": "contracted_rate_per_night",
                "data": [
                    {
                        "range": {
                            "min": 0,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            },
            {
                "name": "number_of_nights",
                "data": [
                    {
                        "range": {
                            "min": 0,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            },
            {
                "name": "booking_anticipation",
                "data": [
                    {
                        "range": {
                            "min": 0,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            },
            {
                "name": "contracted_cancellation_policy",
                "data": [
                    {
                        "type": "basic",
                        "score": 25
                    }
                ]
            },
            {
                "name": "meal_plan_contracted",
                "data": [
                    {
                        "type": "basic",
                        "score": 25
                    }
                ]
            }
        ]
    },
    {
        "name": "purchase_of_extra_services",
        "data": [
            {
                "name": "service_type",
                "data": [
                    {
                        "type": "basic",
                        "socore": 25
                    }
                ]
            },
            {
                "name": "amount_of_upsellings_contracted",
                "data": [
                    {
                        "range": {
                            "min": 25,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            },
            {
                "name": "number_of_upsellings_purchased",
                "data": [
                    {
                        "range": {
                            "min": 25,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            },
            {
                "name": "number_of_cross_sellings_purchased",
                "data": [
                    {
                        "range": {
                            "min": 25,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            },
            {
                "name": "amount_of_upsellings_purchased",
                "data": [
                    {
                        "range": {
                            "min": 25,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            }
        ]
    },
    {
        "name": "purchase_in_the_restaurant",
        "data": [
            {
                "name": "product_category",
                "data": [
                    {
                        "type": "basic",
                        "socore": 25
                    }
                ]
            },
            {
                "name": "average_restaurant_ticket",
                "data": [
                    {
                        "range": {
                            "min": 25,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            },
            {
                "name": "time_spent_at_the_table",
                "data": [
                    {
                        "range": {
                            "min": 25,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            },
            {
                "name": "booking_anticipation",
                "data": [
                    {
                        "range": {
                            "min": 25,
                            "max": 25
                        },
                        "score": 25
                    }
                ]
            }
        ]
    }
]

"""


class ScoreCardService(MongoQueries):
    async def get_customer_score_card(self, customer_id: str):
        customer = await self.clients_customer.find_one(
            {"_id": bson.ObjectId(customer_id)}, {"score": 1, "_id": 0}
        )

        return customer if customer else []

    async def put_score_card(self, customer_id: str, data: Any):
        try:
            final_list = [elem.dict() for elem in data]

            await self.clients_customer.update_one(
                {"_id": bson.ObjectId(customer_id)}, {"$set": {"score": final_list}}
            )

            return {"message": "update successfully"}

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Unknow Error, code (187955)")
