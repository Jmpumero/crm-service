from datetime import datetime, timedelta
from typing import Any, List
from collections import OrderedDict
import pymongo
from config.config import Settings
from core.connection.connection import ConnectionMongo as DwConnection
from dateutil.relativedelta import relativedelta

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.errors import BulkWriteError, DuplicateKeyError, OperationFailure


# from src.customer.schemas.get.responses.cross_selling import CrossSellingResponse
from src.customer.schemas.post.bodys.customer_crud import (
    CreateCustomerBody,
    MergeCustomerBody,
)
from src.customer.schemas.post.responses.blacklist import BlackListBodyResponse
from src.customer.schemas.post.responses.cross_selling import (
    CrossSellingCreatedResponse,
)

from starlette.responses import Response
from src.customer.schemas.post.responses.blacklist import BlackListBodyResponse
from fastapi.encoders import jsonable_encoder
from src.customer.schemas.get.responses import blacklist, customers
from src.customer.schemas.get import responses
import pymongo

from pymongo.errors import DuplicateKeyError, BulkWriteError
from config.config import Settings

from typing import Any


from fastapi import HTTPException


class HistorySensorQueries(DwConnection):
    def __init__(self):
        super().__init__()

    async def get_history_sensor_1(
        cls, id, skip, limit
    ):  # se decidio por nombres genericos para identificar los sensores, en este caso se refiere al sensor cast
        # print(id)
        try:
            response = cls.customer.aggregate(
                [
                    {
                        "$facet": {
                            "customer_history": [
                                {
                                    "$match": {
                                        "_id": {"$eq": id},
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "cast",
                                        "localField": "_id",
                                        "foreignField": "customer_id",
                                        "as": "cast_details",
                                    }
                                },
                                {"$unwind": "$cast_details"},
                                {
                                    "$lookup": {
                                        "from": "castCore",
                                        "localField": "cast_details.data.kkResource",
                                        "foreignField": "kkResource",
                                        "as": "cast_core",
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "site",
                                        "localField": "cast_core.siteId",
                                        "foreignField": "_id",
                                        "as": "site",
                                    }
                                },
                                {
                                    "$project": {
                                        "name": 1,
                                        "last_name": 1,
                                        "full_name": 1,
                                        "cast_details.data.startDate": 1,
                                        "cast_details.data.endDate": 1,
                                        "cast_details.data.kkResource": 1,
                                        # "cast_core.kkResource": 1,
                                        # "cast_core.siteId": 1,
                                        "site._id": 1,
                                        "site.name": 1,
                                    }
                                },
                                {"$skip": skip},
                                {"$limit": limit},
                            ],
                            "total_items": [
                                {
                                    "$match": {
                                        "_id": {"$eq": id},
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "cast",
                                        "localField": "_id",
                                        "foreignField": "customer_id",
                                        "as": "cast_details",
                                    }
                                },
                                {"$unwind": "$cast_details"},
                                {
                                    "$lookup": {
                                        "from": "castCore",
                                        "localField": "cast_details.data.kkResource",
                                        "foreignField": "kkResource",
                                        "as": "cast_core",
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "site",
                                        "localField": "cast_core.siteId",
                                        "foreignField": "_id",
                                        "as": "site",
                                    }
                                },
                                {
                                    "$project": {
                                        "name": 1,
                                    }
                                },
                                {"$count": "total"},
                            ],
                        }
                    },
                ],
                allowDiskUse=True,
            )

            resp = []

            resp = await response.to_list(length=None)
            # if response != None:
            #     print(id)
            #     print(response)
            #     # for item in await response.to_list(length=None):
            #     #     resp = item

            return resp
        except TypeError as e:
            print(e)
            return resp

    async def get_history_sensor_2(cls, id, skip, limit):  # hotspot

        response = cls.customer.aggregate(
            [
                {
                    "$facet": {
                        "customer_history": [
                            {
                                "$match": {
                                    "_id": {"$eq": id},
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "hotspot",
                                    "localField": "_id",
                                    "foreignField": "customer_id",
                                    "as": "hotspot_details",
                                }
                            },
                            {"$unwind": "$hotspot_details"},
                            {
                                "$lookup": {
                                    "from": "wifi",
                                    "localField": "hotspot_details.data.wifiId",
                                    "foreignField": "_id",
                                    "as": "wifi_details",
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "site",
                                    "localField": "wifi_details.siteId",
                                    "foreignField": "_id",
                                    "as": "site",
                                }
                            },
                            {
                                "$project": {
                                    # "name": 1,
                                    # "last_name": 1,
                                    # "full_name": 1,
                                    "hotspot_details.data": 1,
                                    "wifi_details": 1,
                                    "site._id": 1,
                                    "site.name": 1,
                                }
                            },
                            {"$skip": skip},
                            {"$limit": limit},
                        ],
                        "total_items": [
                            {
                                "$match": {
                                    "_id": {"$eq": id},
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "hotspot",
                                    "localField": "_id",
                                    "foreignField": "customer_id",
                                    "as": "hotspot_details",
                                }
                            },
                            {"$unwind": "$hotspot_details"},
                            {
                                "$lookup": {
                                    "from": "wifi",
                                    "localField": "hotspot_details.data.wifiId",
                                    "foreignField": "_id",
                                    "as": "wifi_details",
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "site",
                                    "localField": "wifi_details.siteId",
                                    "foreignField": "_id",
                                    "as": "site",
                                }
                            },
                            {
                                "$project": {
                                    "name": 1,
                                }
                            },
                            {"$count": "total"},
                        ],
                    }
                },
            ],
            allowDiskUse=True,
        )

        resp = []
        if response != None:
            for item in await response.to_list(length=None):
                resp = item
            # print(resp)

        return resp
