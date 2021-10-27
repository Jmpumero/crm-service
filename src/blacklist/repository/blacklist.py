from typing import Any

from src.customer.repository import MongoQueries

blacklist_customer_projections = {
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

    def blacklist_search(self, type, skip, limit):

        cursor = None

        if type == "enable":
            cursor = (
                self.customer.find(
                    {"blacklist_status": False, "customer_status": True},
                    blacklist_customer_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        elif type == "disable":
            cursor = (
                self.customer.find(
                    {"blacklist_status": True, "customer_status": True},
                    blacklist_customer_projections,
                )
                .skip(skip)
                .limit(limit)
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
