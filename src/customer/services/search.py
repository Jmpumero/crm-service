from pydantic.fields import T
from datetime import datetime, timedelta
from fastapi import status
from fastapi.responses import JSONResponse
from core.connection.connection import ConnectionMongo
from src.segmenter.schemas.get import response
from ..repositories import SearchQueries


class SearchService:
    def __init__(self):
        self.repository = SearchQueries()

    def calculated_age(self, date):
        _time = None
        today = today = datetime.utcnow()
        age = None
        if date != None and date != "":
            try:
                _time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")

            except Exception as e:
                try:
                    _time = datetime.strptime(date, "%Y-%m-%d")
                except Exception as e:
                    _time = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")

            age = today - _time

            age = int(age.total_seconds() * 1000)

        return age

    def set_age(self, data):
        for i in range(len(data[0]["items"])):

            t = self.calculated_age(data[0]["items"][i]["birthdate"])
            if t != None:
                data[0]["items"][i]["age"] = t
            else:  # eliminar despues
                data[0]["items"][i]["age"] = None

    def build_response_search(self, data):
        response = {}
        if data != None and len(data[0]["items"]) > 0:

            response["total_items"] = data[0]["total_items"][0]["total"]
            response["total_shows"] = data[0]["total_items_show"][0]["total_show"]
            response["items"] = data[0]["items"]
        else:
            response["total_items"] = 0
            response["total_shows"] = 0
            response["items"] = []
        return response

    async def get_customers(self, skip, limit, q, order_sort, column_sort):
        # agregar lower case?
        r = None
        cursor = self.repository.find_customers(skip, limit, q, order_sort, column_sort)

        if cursor != None:
            r = await cursor.to_list(length=limit)
            self.set_age(r)

        return self.build_response_search(r)
