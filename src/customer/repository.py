import pymongo
from core.connection.connection import ConnectionMongo as DwConnection

from config.config import Settings

from typing import Any


from fastapi import HTTPException
from error_handlers.bad_gateway import BadGatewayException


global_settings = Settings()

search_projections = {
    "_id": 0,
    "name": 1,
    "last_name": 1,
    "full_name": 1,
    "age": 1,
    "nationality": 1,
    "civilStatus": 1,
    "documentId": 1,
    "phone": 1,
    "email": 1,
    "address": 1,
}


class MongoQueries(DwConnection):

    # Metodos de Queries para el servicio de Clientes

    def total_customer(self):
        customers = self.clients_collection.estimated_document_count()
        return customers

    def find_one_customer(self, client_id):
        customer = self.clients_collection.find_one(
            {"id": client_id}, search_projections
        )
        return customer

    def find_all_customers(self, skip, limit, column, order):
        if column:
            if order.lower() == "desc":

                customers = (
                    self.clients_collection.find({}, search_projections)
                    .skip(skip)
                    .limit(limit)
                    .sort(column, pymongo.DESCENDING)
                )
            else:

                customers = (
                    self.clients_collection.find({}, search_projections)
                    .skip(skip)
                    .limit(limit)
                    .sort(column, pymongo.ASCENDING)
                )
        else:
            customers = (
                self.clients_collection.find(
                    {},
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        return customers

    # def insert_one_customer(self, data):
    #     inserted_customer = self.clients_collection.insert_one(data.dict())
    #     return inserted_customer

    def filter_search_customers(self, constrain, item_search, column, skip, limit):

        response = ""
        if constrain == "contain":

            # busca en el campo nombre, aquellos que contenga  'variable' en minscula y mayuscula
            response = (
                self.clients_collection.find(
                    {
                        f"{column}": {
                            "$regex": f".*{item_search}.*|.*{item_search.capitalize()}.*"
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "equal_to":

            return (
                self.clients_collection.find(
                    {f"{column}": {"$eq": f"{item_search}"}}, search_projections
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            return (
                self.clients_collection.find(
                    {
                        f"{column}": {
                            "$regex": f"\A{item_search}|\A{item_search.capitalize()}"
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "ends_by":
            return (
                self.clients_collection.find(
                    {
                        f"{column}": {
                            "$regex": f"\Z{item_search}|\Z{item_search.capitalize()}"
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        return response
