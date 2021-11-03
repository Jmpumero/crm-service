from typing import Any
from datetime import datetime

from fastapi.param_functions import Query


from ..schemas import UpdatedSegment
from core.connection.connection import ConnectionMongo


class DemographyRepo(ConnectionMongo):
    def __init__(self):
        super().__init__()
        self.date_projection = {
            "name": 1,
            "last_name": 1,
            "full_name": 1,
            "nationality": 1,
            "phone": 1,
            "address": 1,
            "postal_address": 1,
            "email": 1,
            "documentId": 1,
            "civil_status": 1,
            "age": 1,
            "birthdate": 1,
            "language": 1,
            "signature": 1,
            "social_media": 1,
            "customer_avatar": 1,
            "customer_status": 1,
            "blacklist_status": 1,
            "associated_sensors": 1,
            "country": 1,
            "city": 1,
            "postalCode": 1,
            "blacklist_last_enable_motive": 1,
            "blacklist_last_disable_motive": 1,
            "general_score": 1,
            "stenant": 1,
            "gender": 1,
            "profession": 1,
            "total_childens": 1,
            "create_at": {"$dateFromString": {"dateString": "$create_at"}},
            "update_at": {"$dateFromString": {"dateString": "$update_at"}},
        }

    async def generic_query(self):
        ...

    def milliseconds_to_string(self, date):

        ms = date
        new_date = datetime.fromtimestamp(ms / 1000.0)
        new_date = datetime.strftime(new_date, "%Y-%m-%dT%H:%M:%S.%f")
        return new_date

    def milliseconds_to_date(self, date):

        ms = date
        new_date = datetime.fromtimestamp(ms / 1000.0)

        return new_date

    def builder_date_query_project(self):

        query_project = {}
        query_project["$project"] = self.date_projection

        return query_project

    def builder_generic_query(self, key, value, status):

        if status:
            query = {"$match": {f"{key}": f"{value}"}}
        else:
            query = {"$match": {"$nor": [{f"{key}": f"{value}"}]}}

        return query

    def build_basic_query_create_at(self, status, operator, date):

        if status:
            query = {"$match": {"create_at": {f"{operator}": date}}}
        else:
            query = {"$match": {"$nor": [{"create_at": {f"{operator}": date}}]}}
        return query

    def builder_data_range(self, status, condition, date=None, from_=None, to_=None):
        if condition == "Between":
            if status:
                query = {"$match": {"create_at": {"$gte": from_, "$lt": to_}}}
            else:
                query = {
                    "$match": {"$nor": [{"create_at": {"$gte": from_, "$lt": to_}}]}
                }
        elif condition == "Equal to":
            print(date)
            query = self.build_basic_query_create_at(status, "$eq", date)
        elif condition == "Less to":
            query = self.build_basic_query_create_at(status, "$lt", date)

        return query

    async def test_alfa_query(self, match):

        return self.customer.aggregate([match, {"$limit": 2}])

    async def test_beta_query(self, data, from_, to_):

        return self.customer.aggregate(
            [
                self.builder_date_query_project(),
                self.builder_data_range(
                    True,
                    data["register_date"]["condition"],
                    self.milliseconds_to_date(data["register_date"]["date"]),
                    from_,
                    to_,
                ),
                {"$limit": 5},
            ]
        )

    async def date_range_query(self, data):

        from_ = self.milliseconds_to_date(data["register_date"]["date_range"]["from_"])
        to_ = self.milliseconds_to_date(data["register_date"]["date_range"]["to"])
        print(from_)
        print(to_)

        result = await self.test_beta_query(data, from_, to_)
        r = await result.to_list(length=None)

        return r
