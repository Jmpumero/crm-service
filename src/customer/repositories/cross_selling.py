from fastapi.encoders import jsonable_encoder
import pymongo

from src.customer.repository import MongoQueries


class CrossSellingQueries(MongoQueries):
    def __init__(self):
        super().__init__()

    async def insert_one_cross_selling_product(self, data):
        resp = None
        product = jsonable_encoder(data)

        if data.name != "":
            resp = await self.products.insert_one(product)

        return resp

    async def insert_many_cross_selling(self, data):

        inserted_product = None
        array_cs = jsonable_encoder(data.news_cross_selling)
        inserted_product = await self.cross_selling.insert_many(array_cs)
        return inserted_product

    async def get_all_cross_selling(cls, data):

        return (
            cls.cross_selling.find({})
            .skip(data.skip)
            .limit(data.limit)
            .sort("principal_product", pymongo.ASCENDING)
        )

    async def get_all_products(cls):
        return cls.products.find({}).sort("name", pymongo.ASCENDING)

    def get_total_cross_selling(cls):
        return cls.cross_selling.count_documents({})

    async def delete_one_cross_selling(cls, id):

        return await cls.cross_selling.find_one_and_delete({"_id": id})
