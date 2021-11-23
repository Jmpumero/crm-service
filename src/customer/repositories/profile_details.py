from fastapi.encoders import jsonable_encoder
import pymongo
from core.connection.connection import ConnectionMongo


class PDQueries(ConnectionMongo):
    def __init__(self):
        super().__init__()
        self.pjt_contact = {"email": 1, "phone": 1, "address": 1, "social_media": 1}

    async def get_contact(self, customer_id):
        customer = await self.customer.find_one({"_id": customer_id}, self.pjt_contact)
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

        return await most_used_guest.to_list(length=None)

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
        for i in range(len(array)):

            if array[i]["count"] > gt:
                gt = array[i]["count"]
                gt_i = i

        return array[gt_i]

    async def get_most_visited_hotel(self, customer_id):

        r = await self.most_visited_h(customer_id, "guest")
        t = await self.most_visited_h(customer_id, "")
        k = self.clear_group_array(r + t)
        # print(self.get_most_coincidence_hotel(k))

        return self.get_most_coincidence_hotel(k)
