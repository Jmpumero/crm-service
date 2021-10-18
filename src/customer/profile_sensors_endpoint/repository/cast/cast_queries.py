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

aggregation_connections = {
    '_id':0, 
    'customer_id':1, 
    'data.startDate': 1
}

aggregation_playback = {
    '_id':0,
    'customer_id': 1,
    'data.playback_pair.metadata.title': 1,
    'data.playback_pair.endDate':1,
    'data.playback_pair.startDate':1,    
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
            result = self.cast_collection.find({'customer_id': customer_id}, aggregation_connections
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
            result = self.cast_collection.find({'customer_id': customer_id}, aggregation_connections).sort([('data.startDate', -1)]).limit(1)
        elif sensor == 'sensor_3':
            result = None
        elif sensor == 'sensor_4':
            result = None

        return result

    def most_used_device(self):
        pass

    def last_playback(self, customer_id):
        result = self.cast_collection.find({'customer_id': customer_id}, aggregation_playback).sort([('data.startDate', -1)]).limit(1)

        return result

    def playback_history(self):
        pass