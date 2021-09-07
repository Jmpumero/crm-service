from core.connection.connection import ConnectionMongo as DwConnection

from config.config import Settings

from typing import Any


from fastapi import HTTPException
from error_handlers.bad_gateway import BadGatewayException


global_settings = Settings()


class MongoQueries(DwConnection):
    # Metodos de Queries para el servicio de Clientes

    def find_one_customer(self, client_id):
        customer = self.clients_collection.find_one({"id": client_id}, {"_id": 0})
        return customer

    def find_all_customers(self):
        customers = self.clients_collection.find({}, {"_id": 0})
        return customers

    def insert_one_customer(self, data):
        inserted_customer = self.clients_collection.insert_one(data.dict())
        return inserted_customer

    def find_customers_by_filter(self):
        pass
