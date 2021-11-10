from bson.son import SON
from pydantic.types import constr

from src.customer.repository import MongoQueries
from config.config import Settings


global_settings = Settings()


class PmsQueries(MongoQueries):
    def __init__(self):
        super().__init__()

    def count_customer_master_books(self, customer_id):
        count = self.pms_collection.count_documents({"customer_id": customer_id})
        return count

    def get_all_customer_stays(self, customer_id):
        match_stage = {
            "$match": {
                "customer_id": customer_id,
            }
        }
        add_date_field_stage = {
            "$addFields": {
                "checkin_date": {"$dateFromString": {"dateString": "$data.checkin"}}
            }
        }
        sort_stage = {"$sort": {"checkin_date": 1}}

        pipeline = [match_stage, add_date_field_stage, sort_stage]
        result = self.pms_collection.aggregate(pipeline)

        return result

    def group_by_most_used_roomType(self, customer_id, customer_type):
        match_stage = {"$match": {"customer_id": customer_id}}

        if customer_type == "pms_booker":
            group_stage = {
                "$group": {
                    "_id": "$data.bBooks.riRoomType.name",
                    "count": {"$sum": 1},
                }
            }
        elif customer_type == "pms_pri_guest":
            group_stage = {
                "$group": {
                    "_id": "$data.riRoomType.name",
                    "count": {"$sum": 1},
                }
            }
        sort_stage = {"$sort": SON([("count", -1), ("_id", -1)])}
        pipeline = [match_stage, group_stage, sort_stage]
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

    def get_cancellations(self, customer_id, customer_type):
        match_stage = {"$match": {"customer_id": customer_id}}
        if customer_type == "pms_booker":
            group_stage = {
                "$group": {
                    "_id": "$data.bBooks.coreBookStatus.code",
                    "count": {"$sum": 1},
                },
            }
        elif customer_type == "pms_pri_guest":
            group_stage = {
                "$group": {
                    "_id": "$data.coreBookStatus.code",
                    "count": {"$sum": 1},
                },
            }
        sort_stage = {"$sort": SON([("count", -1), ("_id", -1)])}
        pipeline = [match_stage, group_stage, sort_stage]
        cancellations = self.pms_collection.aggregate(pipeline)

        return cancellations

    def get_preferred_sale_channel(self, customer_id):
        match_stage = {"$match": {"customer_id": customer_id}}
        group_stage = {
            "$group": {
                "_id": "$data.ssaleChannel.name",
                "count": {"$sum": 1},
            },
        }
        sort_stage = {"$sort": SON([("count", -1), ("_id", -1)])}
        pipeline = [match_stage, group_stage, sort_stage]
        sale_channels = self.pms_collection.aggregate(pipeline)

        return sale_channels

    def get_bookings_agg_customer(self, customer_id, constrain, search, skip, limit):
        if constrain.value == "booking":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {
                            "$or": [
                                {"data.bBooks.code": {"$regex": search.lower()}},
                                {"data.bBooks.code": {"$regex": search.upper()}},
                            ]
                        },
                    ]
                }
            }

        elif constrain.value == "date":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {"data.bBooks.checkin": search},
                    ]
                }
            }
        elif constrain.value == "min_amount":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {"data.bBooks.netAmt": {"$gte": float(search)}},
                    ]
                }
            }
        elif constrain.value == "max_amount":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {"data.bBooks.netAmt": {"$lte": float(search)}},
                    ]
                }
            }

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

    def get_bookings_agg_customer_old(
        self, customer_id, constrain, search, skip, limit, customer_type="pms_booker"
    ):

        if customer_type == "pms_booker":
            booking_constrain = "data.bBooks.code"
            date_constrain = "data.bBooks.checkin"
            amount_constrain = "data.bBooks.netAmt"
        elif customer_type == "pms_pri_guest":
            booking_constrain = "data.code"
            date_constrain = "data.checkin"
            amount_constrain = "data.netAmt"

        if constrain.value == "booking":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {
                            "$or": [
                                {booking_constrain: {"$regex": search.lower()}},
                                {booking_constrain: {"$regex": search.upper()}},
                            ]
                        },
                    ]
                }
            }

        elif constrain.value == "date":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {date_constrain: search},
                    ]
                }
            }
        elif constrain.value == "min_amount":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {amount_constrain: {"$gte": float(search)}},
                    ]
                }
            }
        elif constrain.value == "max_amount":
            match_stage = {
                "$match": {
                    "$and": [
                        {"customer_id": customer_id},
                        {amount_constrain: {"$lte": float(search)}},
                    ]
                }
            }

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

    def get_upsellings_food_beverages(self, customer_id, customer_type):
        match_stage = {"$match": {"customer_id": customer_id}}

        if customer_type == "pms_booker":
            project_stage_1 = {
                "$project": {"_id": 1, "data.bBooks": 1},
            }

            unwind_stage_1 = {"$unwind": "$data.bBooks"}

            project_stage_2 = {"$project": {"_id": 1, "data.bBooks.bForecast": 1}}

            unwind_stage_2 = {"$unwind": "$data.bBooks.bForecast"}

            group_stage = {
                "$group": {
                    "_id": "$data.bBooks.bForecast.concept",
                    "count": {"$sum": 1},
                    "total_income": {"$sum": "$data.bBooks.bForecast.netAmt"},
                }
            }

        elif customer_type == "pms_pri_guest":
            project_stage_1 = {
                "$project": {"_id": 1, "data.bForecast": 1},
            }

            unwind_stage_1 = {"$unwind": "$data.bForecast"}

            project_stage_2 = {"$project": {"_id": 1, "data.bForecast": 1}}

            unwind_stage_2 = {"$unwind": "$data.bForecast"}

            group_stage = {
                "$group": {
                    "_id": "$data.bForecast.concept",
                    "count": {"$sum": 1},
                    "total_income": {"$sum": "$data.bForecast.netAmt"},
                }
            }

        # facet = {
        #     "$facet": {
        #         "concept": [match_stage, project_stage],
        #         "total": [match_stage, {"$count": "total"}],
        #     }
        # }

        sort_stage = {"$sort": SON([("count", -1), ("_id", -1)])}

        pipeline = [
            match_stage,
            project_stage_1,
            unwind_stage_1,
            project_stage_2,
            unwind_stage_2,
            group_stage,
            sort_stage,
        ]

        # pipeline = [facet]
        upsellings_food_beverages = self.pms_collection.aggregate(pipeline)

        return upsellings_food_beverages

    def get_food_beverages(self, customer_id, customer_type):
        match_stage = {"$match": {"customer_id": customer_id}}

        if customer_type == "pms_booker":
            group_stage = {
                "$group": {
                    "_id": "$data.bBooks.bForecast.concept",
                    "count": {"$sum": 1},
                    "total_income": {"$sum": "$data.bBooks.bForecast.netAmt"},
                }
            }
        elif customer_type == "pms_pri_guest":
            group_stage = {
                "$group": {
                    "_id": "$data.bForecast.concept",
                    "count": {"$sum": 1},
                    "total_income": {"$sum": "$data.bForecast.netAmt"},
                }
            }
        sort_stage = {"$sort": SON([("count", -1), ("_id", -1)])}
        pipeline = [match_stage, group_stage, sort_stage]
        food_beverages = self.pms_collection.aggregate(pipeline)

        return food_beverages
