from src.customer.schemas.post.responses.customer_crud import CustomerCRUDResponse
from starlette.responses import Response
from src.customer.schemas.post.responses.blacklist import BlackListBodyResponse
from fastapi.encoders import jsonable_encoder
from src.customer.schemas.get.responses import blacklist, customers
from src.customer.schemas.get import responses
import pymongo
from core.connection.connection import ConnectionMongo as DwConnection

from config.config import Settings

from typing import Any


from fastapi import HTTPException
from error_handlers.bad_gateway import BadGatewayException


global_settings = Settings()

search_projections = {
    "name": 1,
    "last_name": 1,
    "full_name": 1,
    "age": 1,
    "nationality": 1,
    "civilStatus": 1,
    "documentId": 1,
    "booking_id": 1,
    "phone": {
        "$arrayElemAt": [
            "$phone",
            {"$indexOfArray": ["$phone.isMain", True]},
        ]
    },
    "email": {
        "$arrayElemAt": [
            "$email",
            {"$indexOfArray": ["$email.isMain", True]},
        ]
    },
    "address": 1,
}

blacklist_customer_projections = {
    "name": 1,
    "last_name": 1,
    "age": 1,
    "email": 1,
    "phone": 1,
    "address": 1,
    "documentId": 1,
    "nationality": 1,
    "civilStatus": 1,
    "languages": 1,
    "birthdate": 1,
    "associated_sensors": 1,
    "blacklist_status": 1,
    "blacklist_enable_motive": 1,
    "blacklist_disable_motive": 1,
}


class MongoQueries(DwConnection):

    # Metodos de Queries para el servicio de Clientes

    def total_customer(self):
        customers = self.clients_customer.estimated_document_count()
        return customers

    def find_one_customer(self, client_id):
        customer = self.clients_customer.find_one({"id": client_id}, search_projections)
        return customer

    def find_all_customers(self, skip, limit, column, order, column_order):
        if column_order:
            if order.lower() == "desc":

                customers = (
                    self.clients_customer.find({}, search_projections)
                    .skip(skip)
                    .limit(limit)
                    .sort(column_order, pymongo.DESCENDING)
                )
            else:

                customers = (
                    self.clients_customer.find({}, search_projections)
                    .skip(skip)
                    .limit(limit)
                    .sort(column, pymongo.ASCENDING)
                )
        else:
            customers = (
                self.clients_customer.find(
                    {},
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        return customers

    def search_customer_name(
        self, constrain, item_search, column, skip, limit, order, column_order
    ):

        response = ""
        if constrain == "contain":

            # busca en el campo nombre, aquellos que contenga  'variable' en minscula y mayuscula
            return (
                self.clients_customer.find(
                    {
                        f"{column}": {
                            "$regex": f".*{item_search}.*",
                            "$options": "i",
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "equal_to":

            return (
                self.clients_customer.find(
                    {f"{column}": {"$eq": f"{item_search}"}}, search_projections
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            return (
                self.clients_customer.find(
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
                self.clients_customer.find(
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

    def search_customer_email(
        self, constrain, item_search, column, skip, limit, order, column_order
    ):
        response = None
        if constrain == "contain":
            response = (
                self.clients_customer.find(
                    {
                        "email": {
                            "$elemMatch": {
                                "email": {
                                    "$regex": f".*{item_search.lower()}.*",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "equal_to":

            response = (
                self.clients_customer.find(
                    {"email": {"email": f"{item_search}", "isMain": True}},
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            response = (
                self.clients_customer.find(
                    {
                        "email": {
                            "$elemMatch": {
                                "email": {
                                    "$regex": f"\A{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "ends_by":
            response = (
                self.clients_customer.find(
                    {
                        "email": {
                            "$elemMatch": {
                                "email": {
                                    "$regex": f"\Z{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        if column_order:

            if order.lower() == "desc":

                return response.sort(column_order, pymongo.DESCENDING)
            else:
                return response.sort(column_order, pymongo.ASCENDING)

        else:
            return response

        # return response

    def search_phone_local(self, constrain, item_search, column, skip, limit):
        response = ""

        if constrain == "contain":
            return (
                self.clients_customer.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": {
                                    "$regex": f".*{item_search.lower()}.*",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "equal_to":

            return (
                self.clients_customer.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": f"{item_search}",
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            return (
                self.clients_customer.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": {
                                    "$regex": f"\A{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "ends_by":
            return (
                self.clients_customer.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": {
                                    "$regex": f"\Z{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        return response

    def search_phone_intl(self, constrain, item_search, column, skip, limit):
        response = ""

        if constrain == "contain":
            return (
                self.clients_customer.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": {
                                    "$regex": f".*\+{item_search.lower()}.*",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "equal_to":

            return (
                self.clients_customer.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": f"\+{item_search}",
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            return (
                self.clients_customer.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": {
                                    "$regex": f"\A\+{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "ends_by":
            return (
                self.clients_customer.find(
                    {
                        "phone": {
                            "$elemMatch": {
                                f"{column}": {
                                    "$regex": f"\Z\+{item_search}",
                                    "$options": "i",
                                },
                                "isMain": True,
                            }
                        }
                    },
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )

        return response

    def filter_search_phone(self, constrain, item_search, column, skip, limit):
        print(item_search)
        if item_search.find("+") > -1:

            item = item_search.replace(" ", "")
            item = item_search.replace("-", "")
            return self.search_phone_intl(constrain, item, "intl_format", skip, limit)
        else:

            item = item_search.replace(" ", "")
            item = item_search.replace("-", "")
            return self.search_phone_local(constrain, item, "local_format", skip, limit)

    def test_agr(
        self, constrain, item_search, column, skip, limit
    ):  # en desarrollo... pruebas con agregaciones
        return self.clients_customer.aggregate(
            [
                {
                    "$match": {
                        "email": {
                            "$elemMatch": {
                                "email": "ablanca@jacidi.com",
                                "isMain": True,
                            }
                        }
                    }
                },
                {
                    "$project": {
                        "_id": 0,
                        "id": 1,
                        "full_name": 1,
                        "age": 1,
                        "nationality": 1,
                        "civilStatus": 1,
                        "documentId": 1,
                        "phone": {
                            "$arrayElemAt": [
                                "$phone",
                                {"$indexOfArray": ["$phone.isMain", True]},
                            ]
                        },
                        "email": {
                            "$arrayElemAt": [
                                "$email",
                                {"$indexOfArray": ["$email.isMain", True]},
                            ]
                        },
                        "address": 1,
                    }
                },
                {"$sort": {"email": 1}},
                {
                    "$project": {
                        "email.isMain": 0,
                        "phone.isMain": 0,
                        "phone.areaCode": 0,
                        "phone.countryCode": 0,
                    }
                },
            ]
        )

    def filter_search_customers(
        self, constrain, item_search, column, skip, limit, order, column_order
    ):

        response = None
        if column == "email":
            response = self.search_customer_email(
                constrain, item_search, column, skip, limit, order, column_order
            )
        elif column == "phone":

            response = self.filter_search_phone(
                constrain, item_search, column, skip, limit
            )

        elif column == "booking_id":
            # no esta definido su estructura(no se sabe como esta representada si es unica o un usuario puede tener n)
            response = self.find_all_customers(skip, limit, column, order, column_order)

        elif column == "prueba":
            response = self.test_agr(constrain, item_search, column, skip, limit)

        else:
            response = self.search_customer_name(
                constrain, item_search, column, skip, limit, order, column_order
            )

        if response:
            if column_order:

                if column_order == "email":
                    column_order = column_order + ".email"

                if column_order == "phone":
                    column_order = column_order + ".intl_format"

                if order.lower() == "desc":
                    print(column_order)
                    return response.sort(column_order, pymongo.DESCENDING)
                else:
                    return response.sort(column_order, pymongo.ASCENDING)

        return response

    def blacklist_search(self, type, skip, limit):

        cursor = None
        if type == "enable":
            cursor = (
                self.clients_customer.find(
                    {"blacklist_status": False}, blacklist_customer_projections
                )
                .skip(skip)
                .limit(limit)
            )
        elif type == "disable":
            cursor = (
                self.clients_customer.find(
                    {"blacklist_status": True}, blacklist_customer_projections
                )
                .skip(skip)
                .limit(limit)
            )

        return cursor

    def total_customer_in_blacklist(self, type):
        total = self.clients_customer.count_documents({"blacklist_status": type})
        return total

    async def update_customer_in_blacklist(self, data) -> BlackListBodyResponse:
        resp = None
        if data.blacklist_status:
            resp = await self.clients_customer.find_one_and_update(
                {"_id": data.id},
                {
                    "$set": {
                        "blacklist_status": data.blacklist_status,
                        "blacklist_enable_motive": data.motives,
                    }
                },
            )
        else:
            resp = await self.clients_customer.find_one_and_update(
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
        return BlackListBodyResponse(**response)

    async def insert_one_customer(self, data):

        inserted_customer = None
        response = None
        customer = jsonable_encoder(data)
        try:
            inserted_customer = await self.clients_customer.insert_one(customer)
        except:
            response = {
                "msg": " Failed inseting Customer ",
                "code": 400,
            }

        if inserted_customer != None:

            if inserted_customer.acknowledged:
                response = {
                    "msg": " Success Customer created ",
                    "code": 200,
                }
            else:
                response = {
                    "msg": " Failed inseting Customer ",
                    "code": 400,
                }

        return CustomerCRUDResponse(**response)
