from typing import Any

from fastapi import HTTPException, Response

from ..repository import MongoQueries


"""
example model of score:

{
    "purchase_recurrence":{
        "range":[
            {
                "min": 0,
                "max": 25,
                "score": 25
            }
        ],
        "date_range": {
            "min": "07/08/2021",
            "max": "27/09/2021"
        }
    },
    "room_reservations":{
        "room_type":[
            {
                "type": "basic",
                "score": 25
            }
        ],
        "contracted_rate_per_night":[
            {
                "range": [
                    {
                        "min": 0,
                        "max": 25,
                        "score": 25
                    }
                ]
            }
        ],
        "number_of_nights":[
            {
                "range": [
                    {
                        "min": 0,
                        "max": 25,
                        "score": 25
                    }
                ]
            }
        ],
        "booking_anticipation": [
            {
                "range": [
                    {
                        "min": 0,
                        "max": 25,
                        "score": 25
                    }
                ]
            }
        ],
        "contracted_cancellation_policy":[
            {
                "type": "basic",
                "score": 25   
            }
        ],
        "meal_plan_contracted":[
            {
                "type": "basic",
                "score": 25
            }
        ]
    },
    "extra_services":{
        "service_type":[
            {
                "type": "basic",
                "socore": 25
            }
        ],
        "upsellings_purchased":[
            {
                "range": [
                    {
                        "min": 0,
                        "max": 25,
                        "score": 25
                    }
                ]
            }
        ],
        "cross_sellings_contracted":[
            {
                "range": [
                    {
                        "min": 0,
                        "max": 25,
                        "score": 25
                    }
                ]
            }
        ],
        "amount_of_upsellings_purchased":[
            {
               "range": [
                    {
                        "min": 0,
                        "max": 25,
                        "score": 25
                    }
                ] 
            }
        ],
    },
    "purchase_in_the_restaurant":[
        {
            "product_category":[
                {
                    "type": "basic",
                    "socore": 25
                }
            ],
            "average_restaurant_ticket":[
                {
                    "range": [
                        {
                            "min": 0,
                            "max": 25,
                            "score": 25
                        }
                    ]
                }
            ],
            "time_spent_at_the_table":[
                {
                    "range": [
                        {
                            "min": 0,
                            "max": 25,
                            "score": 25
                        }
                    ]
                }
            ],
            "booking_anticipation":[
                {
                    "range": [
                        {
                            "min": 0,
                            "max": 25,
                            "score": 25
                        }
                    ]
                }
            ]
        }
    ]
}
"""


class ScoreCardService(MongoQueries):
    def __init__(self):
        super().__init__()

    async def get_customer_score_card(self, customer_id: str) -> Any:
        customer: Any = await self.customer.find_one(
            {"_id": customer_id}, {"score": 1, "_id": 0}
        )

        return customer if customer else []

    async def put_score_card(self, customer_id: str, data: Any):
        try:
            result: Any = await self.customer.update_one(
                {"_id": customer_id}, {"$set": {"score": data.dict()}}
            )

            if result.modified_count:
                return {"message": "update successfully"}

            return {"message": "client not updated"}

        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Unknow Error, code (187955)")
