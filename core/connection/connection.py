import pymongo
from config.config import Settings

from typing import Any

from traceback import print_exc
from dotenv import load_dotenv

from fastapi import HTTPException
from error_handlers.bad_gateway import BadGatewayException

import motor.motor_asyncio


global_settings = Settings()


load_dotenv()


class ConnectionMongo:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            global_settings.mongodb_url
        )

        self.db = self.client.crm

        self.clients_customer = self.db.customer

        self.pms_collection = self.db.pms
        self.cast_collection = self.db.cast
        self.hotspot_collection = self.db.hotspot
        self.butler_collection = self.db.butler

        self.products = self.db.product
        self.cross_selling = self.db.cross_selling
