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

        self.clients_collection = self.db.customer
        self.clients_collection.create_index(
            [("id", pymongo.ASCENDING)], unique=True
        )  # evita inserciones duplicadas

        self.sensors_collection = self.db.sensors
