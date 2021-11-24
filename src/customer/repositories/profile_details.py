from fastapi.encoders import jsonable_encoder
import pymongo
from datetime import datetime
from core.connection.connection import ConnectionMongo


class PDQueries(ConnectionMongo):
    def __init__(self):
        super().__init__()
        self.pjt_contact = {"email": 1, "phone": 1, "address": 1, "social_media": 1}

    async def get_contact(self, customer_id):
        customer = self.customer.aggregate(
            [
                {"$match": {"_id": customer_id}},
                {"$project": self.pjt_contact},
                {"$project": {"_id": 0}},
            ]
        )
        return customer

    async def most_visited_h(self, customer_id, type):

        if type == "guest":
            pipeline = [
                {"$match": {"customer_id": customer_id}},
                {
                    "$group": {
                        "_id": "$data.riRatePlan.sproperty.name",
                        "count": {"$sum": 1},
                    }
                },
                {"$limit": 5},
            ]
        else:
            pipeline = [
                {"$match": {"customer_id": customer_id}},
                {
                    "$group": {
                        "_id": "$data.sproperty.name",
                        "count": {"$sum": 1},
                    }
                },
                {"$limit": 5},
            ]
        most_used_guest = self.pms_collection.aggregate(pipeline)
        if most_used_guest != None:
            return await most_used_guest.to_list(length=None)
        return None

    def clear_group_array(self, k):

        result = []
        for item in k:
            if item["_id"] != None:
                result.append(item)

        return result

    def get_most_coincidence_hotel(self, array):

        i = 0
        gt = 0
        gt_i = 0
        result = None
        if len(array) > 0 and array != None:
            for i in range(len(array)):

                if array[i]["count"] > gt:
                    gt = array[i]["count"]
                    gt_i = i
            result = array[gt_i]
        return result

    async def get_last_checkout_h(self, customer_id, m_hotel):
        # print(m_hotel)
        time_ck = None
        pipeline = [
            {"$match": {"customer_id": customer_id}},
            {
                "$match": {
                    "$or": [
                        {"data.riRatePlan.sproperty.name": m_hotel},
                        {"data.sproperty.name": m_hotel},
                    ]
                }
            },
            {
                "$project": {
                    "data.checkout": {
                        "$dateFromString": {"dateString": "$data.checkout"}
                    }
                }
            },
            {"$sort": {"data.checkout": -1}},
        ]

        last_checkout = self.pms_collection.aggregate(pipeline)
        # print(last_checkout)
        if last_checkout != None:
            r_last_ck = await last_checkout.to_list(length=None)
            time_ck = r_last_ck[0]["data"]["checkout"]

        return time_ck

    async def get_data_tab_profile(self, customer_id):

        delta = None
        date_last_ck = None
        hotel = None
        today = datetime.utcnow()
        response = {"most_v_hotel": None, "recency": None}

        r = await self.most_visited_h(customer_id, "guest")
        t = await self.most_visited_h(customer_id, "")
        k = self.clear_group_array(r + t)
        hotel = self.get_most_coincidence_hotel(k)
        if hotel != None:
            date_last_ck = await self.get_last_checkout_h(customer_id, hotel["_id"])
            response["most_v_hotel"] = hotel["_id"]

        if date_last_ck != None:

            delta = today - date_last_ck
            response["recency"] = int(delta.total_seconds() * 1000)

        return response
