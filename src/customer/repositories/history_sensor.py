from src.customer.repository import MongoQueries

# se decidio por nombres genericos para identificar los sensores
class HistorySensorQueries(MongoQueries):
    def __init__(self):
        super().__init__()

    async def get_history_sensor_1(cls, id, skip, limit):  #  cast

        response = cls.customer.aggregate(
            [
                {
                    "$facet": {
                        "customer_history": [
                            {
                                "$match": {
                                    "_id": {"$eq": id},
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "cast",
                                    "localField": "_id",
                                    "foreignField": "customer_id",
                                    "as": "cast_details",
                                }
                            },
                            {"$unwind": "$cast_details"},
                            {
                                "$lookup": {
                                    "from": "castCore",
                                    "localField": "cast_details.data.kkResource",
                                    "foreignField": "kkResource",
                                    "as": "cast_core",
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "site",
                                    "localField": "cast_core.siteId",
                                    "foreignField": "_id",
                                    "as": "site",
                                }
                            },
                            {
                                "$project": {
                                    "cast_details.data.startDate": 1,
                                    "cast_details.data.endDate": 1,
                                    "cast_details.data.kkResource": 1,
                                    "site._id": 1,
                                    "site.name": 1,
                                }
                            },
                            {"$skip": skip},
                            {"$limit": limit},
                        ],
                        "total_items": [
                            {
                                "$match": {
                                    "_id": {"$eq": id},
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "cast",
                                    "localField": "_id",
                                    "foreignField": "customer_id",
                                    "as": "cast_details",
                                }
                            },
                            {"$unwind": "$cast_details"},
                            {
                                "$lookup": {
                                    "from": "castCore",
                                    "localField": "cast_details.data.kkResource",
                                    "foreignField": "kkResource",
                                    "as": "cast_core",
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "site",
                                    "localField": "cast_core.siteId",
                                    "foreignField": "_id",
                                    "as": "site",
                                }
                            },
                            {
                                "$project": {
                                    "name": 1,
                                }
                            },
                            {"$count": "total"},
                        ],
                    }
                },
            ],
            allowDiskUse=True,
        )

        resp = []

        resp = await response.to_list(length=None)

        return resp

    async def get_history_sensor_2(cls, id, skip, limit):  # hotspot

        response = cls.customer.aggregate(
            [
                {
                    "$facet": {
                        "customer_history": [
                            {
                                "$match": {
                                    "_id": {"$eq": id},
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "hotspot",
                                    "localField": "_id",
                                    "foreignField": "customer_id",
                                    "as": "hotspot_details",
                                }
                            },
                            {"$unwind": "$hotspot_details"},
                            {
                                "$lookup": {
                                    "from": "wifi",
                                    "localField": "hotspot_details.data.wifiId",
                                    "foreignField": "_id",
                                    "as": "wifi_details",
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "site",
                                    "localField": "wifi_details.siteId",
                                    "foreignField": "_id",
                                    "as": "site",
                                }
                            },
                            {
                                "$project": {
                                    "hotspot_details.data": 1,
                                    "wifi_details": 1,
                                    "site._id": 1,
                                    "site.name": 1,
                                }
                            },
                            {"$skip": skip},
                            {"$limit": limit},
                        ],
                        "total_items": [
                            {
                                "$match": {
                                    "_id": {"$eq": id},
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "hotspot",
                                    "localField": "_id",
                                    "foreignField": "customer_id",
                                    "as": "hotspot_details",
                                }
                            },
                            {"$unwind": "$hotspot_details"},
                            {
                                "$lookup": {
                                    "from": "wifi",
                                    "localField": "hotspot_details.data.wifiId",
                                    "foreignField": "_id",
                                    "as": "wifi_details",
                                }
                            },
                            {
                                "$lookup": {
                                    "from": "site",
                                    "localField": "wifi_details.siteId",
                                    "foreignField": "_id",
                                    "as": "site",
                                }
                            },
                            {
                                "$project": {
                                    "name": 1,
                                }
                            },
                            {"$count": "total"},
                        ],
                    }
                },
            ],
            allowDiskUse=True,
        )

        resp = await response.to_list(length=None)

        return resp
