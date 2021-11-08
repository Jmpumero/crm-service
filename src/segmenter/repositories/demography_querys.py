from typing import Any, Type
from datetime import date, datetime

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
            "birthdate": {"$dateFromString": {"dateString": "$birthdate"}},
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

    def build_basic_query_(self, status, column, operator, date):

        if status:
            query = {"$match": {f"{column}": {f"{operator}": date}}}
        else:
            query = {"$match": {"$nor": [{f"{column}": {f"{operator}": date}}]}}
        return query

    def builder_date_range(
        self, status, column, condition, date=None, from_=None, to_=None
    ):
        if condition == "Between":

            if status:

                query = {"$match": {f"{column}": {"$gte": from_, "$lt": to_}}}
            else:
                query = {
                    "$match": {"$nor": [{f"{column}": {"$gte": from_, "$lt": to_}}]}
                }
        elif condition == "Equal to":
            query = self.build_basic_query_(status, column, "$eq", date)
        elif condition == "Less to":
            query = self.build_basic_query_(status, column, "$lt", date)
        elif condition == "Less than or equal to":
            query = self.build_basic_query_(status, column, "$lte", date)
        elif condition == "Greater than":
            query = self.build_basic_query_(status, column, "$gt", date)
        elif condition == "Greater than or equal to":
            query = self.build_basic_query_(status, column, "$gte", date)
        elif condition == "Null":
            query = self.build_basic_query_(status, column, "$eq", "")
        elif condition == "No null":
            query = self.build_basic_query_(status, column, "$eq", "")
            if status:
                query = {"$match": {f"{column}": {"$not": {"$eq": ""}}}}
            else:
                query = {"$match": {f"{column}": {"$eq": ""}}}
        elif condition == "Different to":
            if status:
                query = {"$match": {f"{column}": {"$not": {"$eq": date}}}}
            else:
                query = {"$match": {f"{column}": {"$eq": date}}}
        return query

    def builder_age_range(self, status, from_=None, to_=None):
        if status:
            query = {"$match": {"age": {"$gte": from_, "$lt": to_}}}
        else:
            query = {"$match": {"$nor": [{"age": {"$gte": from_, "$lt": to_}}]}}
        return query

    def builder_language(self, type, array_languages):

        query = {}
        if type == "all":
            query = {"$match": {"languages": {"$all": array_languages}}}
        elif type == "in":
            query = {"$match": {"languages": {"$in": array_languages}}}

        return query

    async def test_alfa_query(self, match):

        return self.customer.aggregate([match, {"$limit": 20}])

    async def test_beta_query(self, data):
        result = None
        match = {}
        match["$match"] = {}
        match["$match"]["languages"] = {"$in": ["ce", "ab"]}

        l = data["languages"]
        v = self.builder_language("all", l)

        result = self.customer.aggregate([v])
        #
        # result = await self.customer.update_many(
        #     {}, {"$rename": {"language": "languages"}}
        # )

        # example date range
        # result = self.customer.aggregate(
        #     [
        #         {"$match": {"birthdate": {"$not": {"$eq": ""}}}},
        #         self.builder_date_query_project(),
        #         self.builder_date_range(
        #             True,
        #             "birthdate",
        #             data["register_date"]["birth_date"]["condition"],
        #             date=self.milliseconds_to_date(
        #                 data["register_date"]["birth_date"]["date"]
        #             ),
        #             from_=self.milliseconds_to_date(
        #                 data["register_date"]["birth_date"]["date_range"]["from_"],
        #             ),
        #             to_=self.milliseconds_to_date(
        #                 data["register_date"]["birth_date"]["date_range"]["to"]
        #             ),
        #         ),
        #         {"$limit": 10},
        #     ]
        # )

        #### date range classic
        # return self.customer.aggregate(
        #     [
        #         self.builder_date_query_project(),
        #         self.builder_date_range(
        #             True,
        #             data["register_date"]["condition"],
        #             self.milliseconds_to_date(data["register_date"]["date"]),
        #             from_,
        #             to_,
        #         ),
        #         {"$limit": 10},
        #     ]
        # )

        # ####age range
        # return self.customer.aggregate(
        #     [
        #         self.builder_age_range(True, from_, to_),
        #         {"$limit": 10},
        #     ]
        # )
        r = None
        if result != None:
            r = await result.to_list(length=None)

        return r

    async def date_range_test(self, data):

        from_ = self.milliseconds_to_date(data["register_date"]["date_range"]["from_"])
        to_ = self.milliseconds_to_date(data["register_date"]["date_range"]["to"])

        result = await self.test_beta_query(data, from_, to_)
        r = await result.to_list(length=None)

        return r

    async def age_range_test(self, data):

        result = await self.test_beta_query(
            data, data["age_range"]["from_"], data["age_range"]["to"]
        )
        r = await result.to_list(length=None)

        return r
