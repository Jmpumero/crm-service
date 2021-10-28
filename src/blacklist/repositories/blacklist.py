from typing import Any

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
    "languages": 1,
    "birthdate": 1,
    "associated_sensors": 1,
    "blacklist_status": 1,
    "blacklist_enable_motive": 1,
    "blacklist_disable_motive": 1,
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
                        # {"blacklist_enable_motive": {"$in": ["/.*err.*/"]}},
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

    def build_query(self, search, status, skip, limit, column, order_sort):

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

    def search_(self, search, status, skip, limit, column_sort, order_sort):

        result = None

        result = self.build_query(search, status, skip, limit, column_sort, order_sort)

        return result

    def blacklist_search(self, query, skip, limit, column_sort, order_sort, status):

        cursor = None

        cursor = self.build_query(
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

    async def update_customer_in_blacklist(self, data):
        resp = None
        if data.blacklist_status:
            resp = await self.customer.find_one_and_update(
                {"_id": data.id},
                {
                    "$set": {
                        "blacklist_status": data.blacklist_status,
                        "blacklist_enable_motive": data.motives,
                    }
                },
            )
        else:
            resp = await self.customer.find_one_and_update(
                {"_id": data.id},
                {
                    "$set": {
                        "blacklist_status": data.blacklist_status,
                        "blacklist_disable_motive": data.motives,
                    }
                },
            )

        if resp != None:
            response = {"msg": " Success Customer Update ", "code": 200}
        else:
            response = {
                "msg": " Failed Customer Update, Customer not found ",
                "code": 400,
            }
        return response

    async def update_customer_in_blacklist(self, data):
        resp = None
        if data.blacklist_status:
            resp = await self.customer.find_one_and_update(
                {"_id": data.id},
                {
                    "$set": {
                        "blacklist_status": data.blacklist_status,
                        "blacklist_enable_motive": data.motives,
                    }
                },
            )
        else:
            resp = await self.customer.find_one_and_update(
                {"_id": data.id},
                {
                    "$set": {
                        "blacklist_status": data.blacklist_status,
                        "blacklist_disable_motive": data.motives,
                    }
                },
            )

        if resp != None:
            response = {"msg": " Success Customer Update ", "code": 200}
        else:
            response = {
                "msg": " Failed Customer Update, Customer not found ",
                "code": 400,
            }
        return response
