from datetime import datetime, timedelta
from typing import Any, List
from collections import OrderedDict
import pymongo
from config.config import Settings
from core.connection.connection import ConnectionMongo as DwConnection
from dateutil.relativedelta import relativedelta
from error_handlers.bad_gateway import BadGatewayException
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
from error_handlers.bad_gateway import BadGatewayException


class HistorySensorQueries(DwConnection):
    def __init__(self):
        super().__init__()

    async def get_customer_sensor_1(
        cls, id
    ):  # se decidio por nombres genericos para identificar los sensores, en este caso se refiere al sensor cast
        print(id)

        response = cls.customer.aggregate(
            [
                {
                    "$facet": {
                        "customer_history": [
                            {
                                "$match": {
                                    "_id": {"$eq": "616d64193bd3e2caaebb12ff"},
                                }
                            },
                            # {"$limit": 10},
                            # {
                            #     "$lookup": {
                            #         "from": "cast",
                            #         "localField": "_id",
                            #         "foreignField": "customer_id",
                            #         "as": "cast_details",
                            #     }
                            # },
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
        # print(response.to_list(length=None))
        # print(resp)
        return resp

    async def test_call(self, id, sensor):
        pass
