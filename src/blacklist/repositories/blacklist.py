from logging import disable, log
from typing import Any, Coroutine
from datetime import datetime

from src.customer.repository import MongoQueries

blacklist_projections = {
    "name": 1,
    "last_name": 1,
    "age": 1,
    "email": 1,
    "phone": 1,
    "address": 1,
    "documentId": 1,
    "nationality": 1,
    "civil_status": 1,
    "customer_avatar": 1,
    "languages": 1,
    "birthdate": 1,
    "associated_sensors": 1,
    "blacklist_status": 1,
    "blacklist_last_enabled_motive": 1,
    "blacklist_last_disabled_motive": 1,
    "customer_status": 1,
    "email_main": {
        "$arrayElemAt": [
            "$email",
            {"$indexOfArray": ["$email.isMain", True]},
        ]
    },
    "phone_main": {
        "$arrayElemAt": [
            "$phone",
            {"$indexOfArray": ["$phone.isMain", True]},
        ]
    },
    "address_main": {
        "$arrayElemAt": [
            "$address",
            {"$indexOfArray": ["$address.isMain", True]},
        ]
    },
}


class BlacklistQueries(MongoQueries):
    def __init__(self):
        super().__init__()

    def build_search_match(self, item) -> dict:

        match = {"$match": {}}
        if item != None:
            match = {
                "$match": {
                    "$or": [
                        {
                            "name": {
                                "$regex": f".*{item}.*",
                                "$options": "i",
                            }
                        },
                        {
                            "email_main.email": {
                                "$regex": f".*{item}.*",
                                "$options": "i",
                            }
                        },
                        {
                            "address_main.main": {
                                "$regex": f".*{item}.*",
                                "$options": "i",
                            }
                        },
                        {
                            "phone_main.intl_format": {
                                "$regex": f".*{item}.*",
                                "$options": "i",
                            }
                        },
                    ]
                }
            }

        return dict(match)

    def set_column_sort(self, column):
        result = "name"

        if column == "email":
            result = "email_main.email"
        if column == "address":
            result = "address_main.address"
        if column == "phone":
            result = "phone_main.phone"

        return result

    def build_get_query(self, search, status, skip, limit, column, order_sort):

        order = 1
        result = None
        search_match = self.build_search_match(search)
        column_sort = self.set_column_sort(column)
        value_status = False

        if status == "disable":
            value_status = True
        if order_sort == "desc":
            order = -1

        result = self.customer.aggregate(
            [
                {
                    "$facet": {
                        "total_items": [
                            {
                                "$match": {
                                    "blacklist_status": value_status,
                                    "customer_status": True,
                                }
                            },
                            {"$project": blacklist_projections},
                            search_match,
                            {"$count": "total"},
                        ],
                        "total_show": [
                            {
                                "$match": {
                                    "blacklist_status": value_status,
                                    "customer_status": True,
                                }
                            },
                            {"$project": blacklist_projections},
                            search_match,
                            {"$skip": skip},
                            {"$limit": limit},
                            {"$count": "total_show"},
                        ],
                        "items": [
                            {
                                "$match": {
                                    "blacklist_status": value_status,
                                    "customer_status": True,
                                }
                            },
                            {"$project": blacklist_projections},
                            search_match,
                            {"$skip": skip},
                            {"$limit": limit},
                            {
                                "$sort": {
                                    f"{column_sort}": order,
                                    "_id": 1,
                                }
                            },
                        ],
                    }
                },
            ]
        )

        return result

    def blacklist_search(self, query, skip, limit, column_sort, order_sort, status):

        cursor = None

        cursor = self.build_get_query(
            query,
            status,
            skip,
            limit,
            column_sort,
            order_sort,
        )

        return cursor

    def total_customer_in_blacklist(self, type):
        total = self.customer.count_documents(
            {"customer_status": True, "blacklist_status": type}
        )
        return total

    def build_query_update(self, blacklist_log, motives, status):

        item = {}
        type = "enable"
        last_motives = "blacklist_last_enabled_motives"
        query = {}

        if status:
            type = "disable"
            last_motives = "blacklist_last_disabled_motives"

        today = datetime.utcnow()
        today = datetime.strftime(today, "%Y-%m-%dT%H:%M:%S.%f")
        item["date"] = today
        item["type"] = type
        item["motives"] = motives
        log = blacklist_log
        log.append(item)

        query["$set"] = {
            "blacklist_status": status,
            f"{last_motives}": motives,
            "blacklist_log": log,
        }

        return query

    async def update_customer(self, data):
        result = None
        response = None
        array = []
        log = []
        item = {}

        customer = await self.customer.find_one(data.id)
        if customer != None:

            query = self.build_query_update(
                customer["blacklist_log"], data.motives, data.new_status
            )

            result = await self.customer.find_one_and_update(
                {"_id": data.id},
                query,
            )

        return result
