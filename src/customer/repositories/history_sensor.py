from datetime import datetime, timedelta
from typing import Any, List
from collections import OrderedDict
import pymongo
from config.config import Settings
from core.connection.connection import ConnectionMongo as DwConnection
from core import startup_result
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


class HistorySensorQueries:
    def __init__(self):
        self.connection = startup_result["mongo_connection"]
        self.customer = self.connection.customer
        self.cross_selling = self.connection.cross_selling
        self.products = self.connection.products
        self.pms_collection = self.connection.pms_collection
        self.butler_collection = self.connection.butler_collection
        self.cast_collection = self.connection.cast_collection

    async def get_customer_sensor_1(
        cls, id, sensor
    ):  # se decidio por nombres genericos para identificar los sensores, en este caso se refiere al sensor cast
        print(id)
        print(sensor)
        # a= self.customer.aggregate([],allowDiskUse=True)

        return print("hola")

    async def test_call(self, id, sensor):
        pass
