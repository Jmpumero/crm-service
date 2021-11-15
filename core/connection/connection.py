import logging

import pymongo
from dotenv import load_dotenv
import motor.motor_asyncio

from config.config import Settings

global_settings = Settings()
log = logging.getLogger("uvicorn")

load_dotenv()


class ConnectionMongo:
    def __init__(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            global_settings.MONGODB_URL
        )

        log.info(
            f"MONGODB: {global_settings.MONGODB_URL[global_settings.MONGODB_URL.find('@')+1:global_settings.MONGODB_URL.find('/', global_settings.MONGODB_URL.find('@'))]}"
        )

        self.db = self.client.crm

        self.customer = self.db.customer

        self.pms_collection = self.db.pms
        self.cast_collection = self.db.cast
        self.hotspot_collection = self.db.hotspot
        self.butler_collection = self.db.butler
        self.creativity = self.db.creativity

        self.products = self.db.product
        self.cross_selling = self.db.cross_selling
        self.cross_selling.create_index(
            [
                ("principal_product._id", pymongo.ASCENDING),
                ("secondary_product._id", pymongo.ASCENDING),
            ],
            unique=True,
        )

        self.segments = self.db.segmenter
