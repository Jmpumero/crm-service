from bson.son import SON
from pydantic.types import constr

from src.customer.repository import MongoQueries
from src.customer.schemas.get import query_params

from config.config import Settings


global_settings = Settings()


class PmsQueries(MongoQueries):
    def __init__(self):
        super().__init__()

    def count_customer_master_books(self, customer_id):
        count = self.pms_collection.count_documents({"customer_id": customer_id})
        return count

    def get_all_customer_stays(self, customer_id):
        result = self.pms_collection.find({"customer_id": customer_id}).sort(
            [("data.checkin", 1)]
        )
        return result

    def group_by_most_used_roomType(self, customer_id):
        pipeline = [
            {"$match": {"customer_id": customer_id}},
            {
                "$group": {
                    "_id": "$data.books.riRoomTypeName",
                    "count": {"$sum": 1},
                }
            },
            {"$sort": SON([("count", -1), ("_id", -1)])},
        ]
        most_used = self.pms_collection.aggregate(pipeline)

        return most_used

    def get_avg_pax(self, customer_id):
        match_stage = {"$match": {"customer_id": customer_id}}

        group_stage = {
            "$group": {
                "_id": "$data.books",
                "count": {"$sum": 1},
                "average": {
                    "$avg": {
                        {
                            "$add": [
                                "$data.books.adults",
                                "$data.books.children",
                                "$data.books.babies",
                            ]
                        }
                    }
                },
            },
        }

        sort_stage = {"$sort": SON([("count", -1), ("_id", -1), ("average", -1)])}
        pipeline = [match_stage, group_stage, sort_stage]
        pax_avg = self.pms_collection.aggregate(pipeline)

        return pax_avg

    def get_cancellations(self, customer_id):
        pipeline = [
            {"$match": {"customer_id": customer_id}},
            {
                "$group": {
                    "_id": "$data.books.coreBookStatusName",
                    "count": {"$sum": 1},
                },
            },
            {"$sort": SON([("count", -1), ("_id", -1)])},
        ]
        cancellations = self.pms_collection.aggregate(pipeline)

        return cancellations

    def get_preferred_sale_channel(self, customer_id):
        pipeline = [
            {"$match": {"customer_id": customer_id}},
            {
                "$group": {
                    "_id": "$data.sSalesChannelName",
                    "count": {"$sum": 1},
                },
            },
            {"$sort": SON([("count", -1), ("_id", -1)])},
        ]
        sale_channels = self.pms_collection.aggregate(pipeline)

        return sale_channels

    def get_bookings_agg_customer(self, customer_id, constrain, search, skip, limit):
        if constrain.value == "Booking":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {
                            "$or": [
                                {"data.code": {"$regex": search.lower()}},
                                {"data.code": {"$regex": search.upper()}},
                            ]
                        },
                    ]
                }
            }

        elif constrain.value == "Fecha":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {"data.checkin": search},
                    ]
                }
            }
        elif constrain.value == "Monto min.":
            pass
        elif constrain.value == "Monto max.":
            pass
        # elif constrain.value == "Monto min.":
        #     match_stage = {
        #         "$match": {
        #             "$and": [
        #                 {"customer_id": customer_id},
        #                 {"data.bBooks.netAmt": {"$gte": float(search)}},
        #             ]
        #         }
        #     }
        # elif constrain.value == "Monto max.":
        #     match_stage = {
        #         "$match": {
        #             "$and": [
        #                 {"customer_id": customer_id},
        #                 {"data.bBooks.netAmt": {"$lte": float(search)}},
        #             ]
        #         }
        #     }

        lookup_customer_stage = {
            "$lookup": {
                "from": "customer",
                "localField": "customer_id",
                "foreignField": "_id",
                "as": "pms_customer",
            }
        }

        skip_stage = {"$skip": skip}

        limit_stage = {"$limit": limit}

        pipeline = [
            match_stage,
            lookup_customer_stage,
            skip_stage,
            limit_stage,
        ]

        result = self.pms_collection.aggregate(pipeline)

        return result
