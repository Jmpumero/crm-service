from bson.son import SON

from src.customer.repository import MongoQueries
from src.customer.schemas.get import query_params

from config.config import Settings


global_settings = Settings()

class PmsQueries(MongoQueries):
    def __init__(self):
        super().__init__()

    def count_customer_master_books(self, customer_id):
        count = self.pms_collection.count_documents({'customer_id': customer_id})
        return count
    
    def get_all_customer_stays(self, customer_id):
        result = self.pms_collection.find({'customer_id': customer_id}).sort([('data.checkin', 1)])
        return result

    def group_by_most_used_roomType(self, customer_id):
        pipeline = [
            {
                '$match': { 'customer_id': customer_id } },
            {
                "$group": {
                    "_id": "$data.bBooks.riRoomType.name", 
                    "count": {"$sum": 1},     
                }
            },
            {
                "$sort": SON([("count", -1), ("_id", -1)])
            }
        ]
        most_used = self.pms_collection.aggregate(pipeline)

        return most_used

    def get_avg_anticipation(self, customer_id):
        pipeline = [
            {
                '$match': { 'customer_id': customer_id } },
            {
                "$group": 
                    {
                        "_id": "$customer_id", 
                        "count": {"$sum": 1},
                        "average": 
                            {
                                '$avg': 
                                    {
                                        '$divide': 
                                            [
                                                {
                                                    '$subtract': 
                                                        [   
                                                            {
                                                                '$dateFromString': {
                                                                    'dateString': "$data.checkin",
                                                                    'format': '%Y-%m-%d'
                                                                } 
                                                            },
                                                            { 
                                                                '$dateFromString': {
                                                                    'dateString': "$data.createdAt",
                                                                } 
                                                            }
                                                        ]
                                                }, 3600000
                                            ]
                                    }       
                            }           
                    },
            },
            {
                "$sort": SON([("count", -1), ("_id", -1), ("average", -1)])
            }

        ]
        most_used = self.pms_collection.aggregate(pipeline)

        return most_used

    def get_cancellations(self, customer_id):
        pipeline = [
            {
                '$match': { 'customer_id': customer_id } },
            {
                "$group": 
                    {
                        "_id": "$data.bBooks.coreBookStatus.code", 
                        "count": {"$sum": 1},           
                    },
            },
            {
                "$sort": SON([("count", -1), ("_id", -1)])
            }
        ]
        cancellations = self.pms_collection.aggregate(pipeline)

        return cancellations

    def get_preferred_sale_channel(self, customer_id):
        pipeline = [
            {
                '$match': { 'customer_id': customer_id } },
            {
                "$group": 
                    {
                        "_id": "$data.ssaleChannel.name", 
                        "count": {"$sum": 1},           
                    },
            },
            {
                "$sort": SON([("count", -1), ("_id", -1)])
            }
        ]
        sale_channels = self.pms_collection.aggregate(pipeline)

        return sale_channels





    