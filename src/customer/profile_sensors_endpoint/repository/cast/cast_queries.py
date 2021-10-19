from datetime import datetime, timedelta
from typing import Any, List
from collections import OrderedDict
from bson.son import SON
from config.config import Settings
from core.connection.connection import ConnectionMongo as DwConnection
from dateutil.relativedelta import relativedelta
from error_handlers.bad_gateway import BadGatewayException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.errors import BulkWriteError, DuplicateKeyError, OperationFailure
from src.customer.repository import MongoQueries
from src.customer.schemas.get import query_params, responses
from src.customer.schemas.get.responses import blacklist, customers, segmenter
from src.customer.schemas.get.responses.segmenter import (
    AuthorsInSegments,
    Segmenter,
    SegmenterResponse,
    SegmenterTable,
)

# from src.customer.schemas.get.responses.cross_selling import CrossSellingResponse
from src.customer.schemas.post.bodys.customer_crud import (
    CreateCustomerBody,
    MergeCustomerBody,
)
from src.customer.schemas.post.responses.blacklist import BlackListBodyResponse
from src.customer.schemas.post.responses.cross_selling import (
    CrossSellingCreatedResponse,
)
from src.customer.schemas.post.responses.customer_crud import CustomerCRUDResponse
from starlette.responses import Response
from src.customer.schemas.post.responses.blacklist import BlackListBodyResponse
from fastapi.encoders import jsonable_encoder
from src.customer.schemas.get.responses import blacklist, customers
from src.customer.schemas.get import responses
import pymongo
from core import startup_result
from pymongo.errors import DuplicateKeyError, BulkWriteError
from config.config import Settings

from typing import Any


from fastapi import HTTPException
from error_handlers.bad_gateway import BadGatewayException


global_settings = Settings()

connections_proy = {
    '_id':0, 
    'customer_id':1, 
    'data.startDate': 1
}

playback_proy = {
    '_id':0,
    'customer_id': 1,
    'data.playback_pair.metadata.title': 1,
    'data.playback_pair.endDate':1,
    'data.playback_pair.startDate':1,    
}

history_proy = {
    '_id': 0,
    'data.startDate': 1,
    'data.playback_pair.appName': 1,
    'data.playback_pair.content': 1,
    'data.playback_pair.startDate': 1,
    'data.playback_pair.endDate': 1,
    'data.deviceId': 1
}

class CastQueries(MongoQueries):
    def __init__(self):
        super().__init__()


    def connection_number(self, customer_id, sensor):
        if sensor == 'sensor_1':
            count = self.pms_collection.count_documents({'customer_id': customer_id})
        elif sensor == 'sensor_2':
            count = self.cast_collection.count_documents({'customer_id': customer_id})
        elif sensor == 'sensor_3':
            count = self.hotspot_collection.count_documents({'customer_id': customer_id})
        elif sensor == 'sensor_4':
            count = self.butler_collection.count_documents({'customer_id': customer_id})

        return count

    def first_connection(self, customer_id, sensor):
        if sensor == 'sensor_1':
            result = None
        elif sensor == 'sensor_2':
            result = self.cast_collection.find({'customer_id': customer_id}, connections_proy
                                               ).sort([('data.startDate', 1)]).limit(1)
        elif sensor == 'sensor_3':
            result = None
        elif sensor == 'sensor_4':
            result = None

        return result

    def last_connection(self, customer_id, sensor):
        if sensor == 'sensor_1':
            result = None
        elif sensor == 'sensor_2':
            result = self.cast_collection.find({'customer_id': customer_id}, connections_proy).sort([('data.startDate', -1)]).limit(1)
        elif sensor == 'sensor_3':
            result = None
        elif sensor == 'sensor_4':
            result = None

        return result

    def last_playback(self, customer_id):
        result = self.cast_collection.find({'customer_id': customer_id}, playback_proy).sort([('data.startDate', -1)]).limit(1)

        return result

    def playback_history(self, customer_id, sensor):
        if sensor == 'sensor_1':
            result = None
        elif sensor == 'sensor_2':
            result = self.cast_collection.find({'customer_id': customer_id}, history_proy)
        elif sensor == 'sensor_3':
            result = None
        elif sensor == 'sensor_4':
            result = None

        return result

    def group_by_most_used_app(self, customer_id):
        pipeline = [
            {'$match': { 'customer_id': customer_id } },
            {"$group": {"_id": "$data.playback_pair.appName", "count": {"$sum": 1}}},
            {"$sort": SON([("count", -1), ("_id", -1)])}
        ]
        most_used = self.cast_collection.aggregate(pipeline)

        return most_used