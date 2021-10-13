from datetime import datetime, timedelta
from typing import Any, List
from collections import OrderedDict
import pymongo
from config.config import Settings
from core.connection.connection import ConnectionMongo as DwConnection
from dateutil.relativedelta import relativedelta
from error_handlers.bad_gateway import BadGatewayException
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pymongo.errors import BulkWriteError, DuplicateKeyError, OperationFailure
from src.customer.schemas.get import query_params, responses
from src.customer.schemas.get.responses import blacklist, customers, segmenter
from src.customer.schemas.get.responses.segmenter import (
    AuthorsInSegments,
    Segmenter,
    SegmenterResponse,
    SegmenterTable,
)

# from src.customer.schemas.get.responses.cross_selling import CrossSellingResponse
from src.customer.schemas.post.bodys.customer_crud import (
    CreateCustomerBody,
    MergeCustomerBody,
)
from src.customer.schemas.post.responses.blacklist import BlackListBodyResponse
from src.customer.schemas.post.responses.cross_selling import (
    CrossSellingCreatedResponse,
)
from src.customer.schemas.post.responses.customer_crud import CustomerCRUDResponse
from starlette.responses import Response
from src.customer.schemas.post.responses.blacklist import BlackListBodyResponse
from fastapi.encoders import jsonable_encoder
from src.customer.schemas.get.responses import blacklist, customers
from src.customer.schemas.get import responses
import pymongo
from core import startup_result
from pymongo.errors import DuplicateKeyError, BulkWriteError
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
    "civil_status": 1,
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
    "civil_status": 1,
    "languages": 1,
    "birthdate": 1,
    "associated_sensors": 1,
    "blacklist_status": 1,
    "blacklist_enable_motive": 1,
    "blacklist_disable_motive": 1,
}

# search_update_projections = {"blacklist_status": 0}


class MongoQueries:
    def __init__(self):
        self.connection = startup_result["mongo_connection"]
        self.customer = self.connection.customer
        self.cross_selling = self.connection.cross_selling
        self.products = self.connection.products
        self.pms_collection = self.connection.pms_collection
        self.butler_collection = self.connection.butler_collection
        self.cast_collection = self.connection.cast_collection

    # Metodos de Queries para el servicio de Clientes

    def total_customer(self):
        total_customers = self.customer.count_documents({"customer_status": True})
        return total_customers

    def find_one_customer(self, client_id):
        customer = self.customer.find_one({"id": client_id}, search_projections)
        return customer

    def find_all_customers(self, skip, limit, column, order, column_order):
        if column_order:
            if order.lower() == "desc":

                customers = (
                    self.customer.find({}, search_projections)
                    .skip(skip)
                    .limit(limit)
                    .sort(column_order, pymongo.DESCENDING)
                )
            else:

                customers = (
                    self.customer.find({}, search_projections)
                    .skip(skip)
                    .limit(limit)
                    .sort(column, pymongo.ASCENDING)
                )
        else:
            customers = (
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
                    {f"{column}": {"$eq": f"{item_search}"}}, search_projections
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            return (
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
                    {"email": {"email": f"{item_search}", "isMain": True}},
                    search_projections,
                )
                .skip(skip)
                .limit(limit)
            )
        if constrain == "starts_by":
            response = (
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
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
                self.customer.find(
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
        # print(type)
        if type == "enable":
            cursor = (
                self.customer.find(
                    {"blacklist_status": False}, blacklist_customer_projections
                )
                .skip(skip)
                .limit(limit)
            )
        elif type == "disable":
            cursor = (
                self.customer.find(
                    {"blacklist_status": True}, blacklist_customer_projections
                )
                .skip(skip)
                .limit(limit)
            )

        return cursor

    def total_customer_in_blacklist(self, type):
        total = self.customer.count_documents(
            {"customer_status": True, "blacklist_status": type}
        )
        return total

    async def update_customer_in_blacklist(self, data) -> BlackListBodyResponse:
        resp = None
        if data.blacklist_status:
            resp = await self.customer.find_one_and_update(
                {"_id": data.id},
                {
                    "$set": {
                        "blacklist_status": data.blacklist_status,
                        "blacklist_enable_motive": data.motives,
                    }
                },
            )
        else:
            resp = await self.customer.find_one_and_update(
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
        customer = dict(data)
        today = datetime.utcnow()
        today = datetime.strftime(today, "%Y-%m-%dT%H:%M:%S")
        customer["create_at"] = today
        customer["update_at"] = today
        customer = CreateCustomerBody(**customer)

        customer = jsonable_encoder(customer)

        try:
            inserted_customer = await self.customer.insert_one(customer)
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

    def find_all_customers_in_crud_view(
        self, skip, limit, column_sort, order, special_query
    ):

        if column_sort:
            if order.lower() == "desc":

                customers = (
                    self.customer.find(special_query)
                    .skip(skip)
                    .limit(limit)
                    .sort(column_sort, pymongo.DESCENDING)
                )
            else:

                customers = (
                    self.customer.find(special_query)
                    .skip(skip)
                    .limit(limit)
                    .sort(column_sort, pymongo.ASCENDING)
                )

        return customers

    def find_filter_customers_in_crud_view(
        self, query, skip, limit, column_sort, order
    ):

        customers = (
            self.customer.find(
                {
                    "$and": [
                        {"customer_status": True},
                        {
                            "$or": [
                                {
                                    "full_name": {
                                        "$regex": f".*{query}.*",
                                        "$options": "i",
                                    }
                                },
                                {
                                    "name": {
                                        "$regex": f".*{query}.*",
                                        "$options": "i",
                                    }
                                },
                                {
                                    "email": {
                                        "$elemMatch": {
                                            "email": {
                                                "$regex": f".*{query}.*",
                                                "$options": "i",
                                            },
                                            "isMain": True,
                                        }
                                    }
                                },
                                {
                                    "phone": {
                                        "$elemMatch": {
                                            "intl_format": {
                                                "$regex": f".*\+{query}.*",
                                                "$options": "i",
                                            },
                                            "isMain": True,
                                        }
                                    }
                                },
                                {
                                    "phone": {
                                        "$elemMatch": {
                                            "local_format": {
                                                "$regex": f".*{query}.*",
                                                "$options": "i",
                                            },
                                            "isMain": True,
                                        }
                                    }
                                },
                            ]
                        },
                    ]
                },
            )
            .skip(skip)
            .limit(limit)
        )
        if order.lower() == "desc":
            customers.sort(column_sort, pymongo.DESCENDING)
        else:
            customers.sort(column_sort, pymongo.ASCENDING)

        return customers

    def build_query_update(self, data):
        query = {}
        today = datetime.utcnow()
        today = datetime.strftime(today, "%Y-%m-%dT%H:%M:%S")
        if data.name != "" and data.name != None:
            query["name"] = data.name
        if data.last_name != "" and data.last_name != None:
            query["last_name"] = data.last_name
        if data.full_name != "" and data.full_name != None:
            query["full_name"] = data.full_name
        if data.nationality != "" and data.nationality != None:
            query["nationality"] = data.nationality
        if data.phone != "" and data.phone != None:

            for i in data.phone:
                query["phone"] = [i.dict() for i in data.phone]

        if data.address != "" and data.address != None:
            query["address"] = data.address
        if data.postal_address != "" and data.postal_address != None:
            query["postal_address"] = data.postal_address
        if data.email != "" and data.email != None:

            for i in data.email:
                query["email"] = [i.dict() for i in data.email]

        if data.documentId != "" and data.documentId != None:
            for i in data.documentId:
                query["documentId"] = [i.dict() for i in data.documentId]

        if data.civil_status != "" and data.civil_status != None:
            query["civil_status"] = data.civil_status
        if data.age != "" and data.age != None:
            query["age"] = data.age
        if data.birthdate != "" and data.birthdate != None:
            query["birthdate"] = data.birthdate

        if data.language != "" and data.language != None:
            for i in data.language:
                query["language"] = [i.dict() for i in data.language]

        if data.social_media != "" and data.social_media != None:
            for i in data.social_media:
                query["social_media"] = [i.dict() for i in data.social_media]

        if data.customer_avatar != "" and data.customer_avatar != None:
            query["customer_avatar"] = data.customer_avatar
        if data.signature != "" and data.signature != None:
            query["name"] = data.signature
        query["last_update"] = today
        return query

    async def update_customer_(self, data):

        query = self.build_query_update(data)
        resp = None
        if data.id != "" and data.id != None:
            resp = await self.customer.find_one_and_update(
                {"_id": data.id},
                {"$set": query},
            )

        if resp != None:
            resp = {"msg": " Success Customer Update ", "code": 200}
        else:
            resp = {
                "msg": " Failed Customer Update, Customer not found ",
                "code": 400,
            }
        return resp

    async def update_many_customer_in_sensors(
        self, old_customer_id, new_customer_id, sensors
    ):

        for i in range(0, len(sensors)):

            if sensors[i] == "sensor_1":
                await self.pms_collection.update_many(
                    {"customer_id": old_customer_id},
                    {"$set": {"customer_id": new_customer_id}},
                )
            elif sensors[i] == "sensor_2":
                await self.cast_collection.update_many(
                    {"customer_id": old_customer_id},
                    {"$set": {"customer_id": new_customer_id}},
                )
            elif sensors[i] == "sensor_3":
                await self.hotspot_collection.update_many(
                    {"customer_id": old_customer_id},
                    {"$set": {"customer_id": new_customer_id}},
                )
            elif sensors[i] == "sensor_4":
                await self.butler_collection.update_many(
                    {"customer_id": old_customer_id},
                    {"$set": {"customer_id": new_customer_id}},
                )

    async def hard_delete_customer(self, customer_id):
        return await self.customer.find_one_and_delete({"_id": customer_id})

    async def delete_one_customer(self, customer_id):

        r_query = None
        customer = None
        customer = await self.customer.find_one({"_id": customer_id})

        today = datetime.utcnow()
        today = datetime.strftime(today, "%Y-%m-%dT%H:%M:%S")

        if customer:
            if customer["associated_sensors"]:
                if len(customer["associated_sensors"]) > 0:
                    r_query = await self.customer.find_one_and_update(
                        {"_id": customer_id},
                        {"$set": {"customer_status": False, "delete_at": today}},
                    )
                else:
                    r_query = await self.customer.find_one_and_delete(
                        {"_id": customer_id}
                    )
            else:
                r_query = await self.customer.find_one_and_delete({"_id": customer_id})

        return customer

    async def merge_customers(self, data):
        id_parent_a = data.id_parent_a
        id_parent_b = data.id_parent_b
        body = dict(data)

        customer = {
            k: v for k, v in body.items() if k not in ["id_parent_a", "id_parent_b"]
        }
        await self.hard_delete_customer(id_parent_a)
        await self.hard_delete_customer(id_parent_b)
        today = datetime.utcnow()
        today = datetime.strftime(today, "%Y-%m-%dT%H:%M:%S")
        customer["create_at"] = today
        customer["update_at"] = today
        customer = CreateCustomerBody(**customer)
        customer = jsonable_encoder(customer)
        new_customer = await self.customer.insert_one(customer)

        await self.update_many_customer_in_sensors(
            id_parent_a, new_customer.inserted_id, data.associated_sensors
        )
        await self.update_many_customer_in_sensors(
            id_parent_b, new_customer.inserted_id, data.associated_sensors
        )

        if new_customer.inserted_id != None:
            resp = {"msg": " Success customers Merge", "code": 200}
        else:
            resp = {
                "msg": " Failed Customers Merge ",
                "code": 400,
            }
        return resp

    async def insert_one_cross_selling_product(self, data):

        inserted_product = None
        response = None

        product = jsonable_encoder(data)

        try:
            inserted_product = await self.products.insert_one(product)
        except:
            response = {
                "msg": " Failed inseting Product ",
                "code": 400,
            }

        if inserted_product != None:

            if inserted_product.acknowledged:
                response = {
                    "msg": " Success Product created ",
                    "code": 200,
                }
            else:
                response = {
                    "msg": " Failed inseting Customer ",
                    "code": 400,
                }

        return CrossSellingCreatedResponse(**response)

    async def insert_many_cross_selling(self, data):

        inserted_product = None
        response = None
        duplicate_items = []

        array_cs = jsonable_encoder(data.news_cross_selling)

        try:
            inserted_product = await self.cross_selling.insert_many(array_cs)

            if inserted_product.acknowledged:
                response = {
                    "msg": " Success Cross Selling created ",
                    "code": 200,
                }

        except BulkWriteError as e:  # fallo al intetar escribir por llaves duplicadas

            # print(e.details["writeErrors"])
            duplicate_items.append(
                e.details["writeErrors"][0]["op"]["principal_product"]["name"]
            )
            duplicate_items.append(
                e.details["writeErrors"][0]["op"]["secondary_product"]["name"]
            )

            response = {
                "msg": " Failed inserting Cross Selling, duplicate keys ",
                "code": 406,
                "details": duplicate_items,
            }

        except Exception as e:
            response = {
                "msg": " Failed inserting Cross Selling, desconocido ",
                "code": 410,
                "details": e.details["writeErrors"][0],
            }

        return response

    async def get_all_cross_selling(self, data):

        return (
            self.cross_selling.find({})
            .skip(data.skip)
            .limit(data.limit)
            .sort("principal_product", pymongo.ASCENDING)
        )

    async def get_all_products(self):
        return self.products.find({}).sort("name", pymongo.ASCENDING)

    def get_total_cross_selling(self):
        return self.cross_selling.count_documents({})

    async def find_segments(self, params) -> Any:
        r = None
        order = 1
        column_target = "name"

        if params.order_sort == "desc":
            order = -1
        if params.column_sort.lower() == "":
            column_target = "name"
        elif params.column_sort.lower() == "author":
            column_target = "author_details.name"
        elif params.column_sort.lower() == "ultima actualizacion":
            column_target = "update_at"
        elif params.column_sort.lower() == "estado":
            column_target = "status"
        elif params.column_sort.lower() == "fecha de creacion":
            column_target = "created_at"
        elif params.column_sort.lower() == "clientes":
            column_target = "clients"

        if params.author == "" and params.tag == "":

            r = self.segments.aggregate(
                [
                    {
                        "$facet": {
                            "total_items": [
                                {
                                    "$lookup": {
                                        "from": "customer",
                                        "localField": "author",
                                        "foreignField": "_id",
                                        "as": "author_details",
                                    }
                                },
                                {"$unwind": "$author_details"},
                                {
                                    "$project": {
                                        "author": 0,
                                        "filter": 0,
                                        "applied_filters": 0,
                                    }
                                },
                                {"$count": "total_items"},
                            ],
                            "total_show": [
                                {
                                    "$lookup": {
                                        "from": "customer",
                                        "localField": "author",
                                        "foreignField": "_id",
                                        "as": "author_details",
                                    }
                                },
                                {"$unwind": "$author_details"},
                                {
                                    "$project": {
                                        "author": 0,
                                        "filter": 0,
                                        "applied_filters": 0,
                                    }
                                },
                                {"$skip": params.skip},
                                {"$limit": params.limit},
                                {"$count": "show_items"},
                            ],
                            "segments": [
                                {
                                    "$lookup": {
                                        "from": "customer",
                                        "localField": "author",
                                        "foreignField": "_id",
                                        "as": "author_details",
                                    }
                                },
                                {"$unwind": "$author_details"},
                                {
                                    "$project": {
                                        "author": 0,
                                        "filter": 0,
                                        "applied_filters": 0,
                                    }
                                },
                                {"$skip": params.skip},
                                {"$limit": params.limit},
                                {
                                    "$sort": {
                                        f"{column_target}": order,
                                        "_id": 1,
                                    }
                                },
                            ],
                        }
                    },
                ]
            )
        elif params.author != "" and params.tag != "":

            tags = params.tag.replace("[", "").replace("]", "").split(",")

            try:
                r = self.segments.aggregate(
                    [
                        {
                            "$facet": {
                                "total_items": [
                                    {
                                        "$match": {
                                            "tags": {"$in": tags},
                                            "author": params.author,
                                        }
                                    },
                                    {
                                        "$lookup": {
                                            "from": "customer",
                                            "localField": "author",
                                            "foreignField": "_id",
                                            "as": "author_details",
                                        }
                                    },
                                    {"$unwind": "$author_details"},
                                    {
                                        "$project": {
                                            "author": 0,
                                            "filter": 0,
                                            "applied_filters": 0,
                                        }
                                    },
                                    {"$count": "total_items"},
                                ],
                                "total_show": [
                                    {
                                        "$match": {
                                            "tags": {"$in": tags},
                                            "author": params.author,
                                        }
                                    },
                                    {
                                        "$lookup": {
                                            "from": "customer",
                                            "localField": "author",
                                            "foreignField": "_id",
                                            "as": "author_details",
                                        }
                                    },
                                    {"$unwind": "$author_details"},
                                    {
                                        "$project": {
                                            "author": 0,
                                            "filter": 0,
                                            "applied_filters": 0,
                                        }
                                    },
                                    {"$skip": params.skip},
                                    {"$limit": params.limit},
                                    {"$count": "show_items"},
                                ],
                                "segments": [
                                    {
                                        "$match": {
                                            "tags": {"$in": tags},
                                            "author": params.author,
                                        }
                                    },
                                    {
                                        "$lookup": {
                                            "from": "customer",
                                            "localField": "author",
                                            "foreignField": "_id",
                                            "as": "author_details",
                                        }
                                    },
                                    {"$unwind": "$author_details"},
                                    {
                                        "$project": {
                                            "author": 0,
                                            "filter": 0,
                                            "applied_filters": 0,
                                        }
                                    },
                                    {"$skip": params.skip},
                                    {"$limit": params.limit},
                                    {
                                        "$sort": {
                                            f"{column_target }": order,
                                            "_id": 1,
                                        }
                                    },
                                ],
                            }
                        },
                    ]
                )
            except Exception as e:
                print(e)
            except OperationFailure as e:
                print(e)

        elif params.author != "" and params.tag == "":
            r = self.segments.aggregate(
                [
                    {
                        "$facet": {
                            "total_items": [
                                {
                                    "$match": {
                                        "author": params.author,
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "customer",
                                        "localField": "author",
                                        "foreignField": "_id",
                                        "as": "author_details",
                                    }
                                },
                                {"$unwind": "$author_details"},
                                {
                                    "$project": {
                                        "author": 0,
                                        "filter": 0,
                                        "applied_filters": 0,
                                    }
                                },
                                {"$count": "total_items"},
                            ],
                            "total_show": [
                                {
                                    "$match": {
                                        "author": params.author,
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "customer",
                                        "localField": "author",
                                        "foreignField": "_id",
                                        "as": "author_details",
                                    }
                                },
                                {"$unwind": "$author_details"},
                                {
                                    "$project": {
                                        "author": 0,
                                        "filter": 0,
                                        "applied_filters": 0,
                                    }
                                },
                                {"$skip": params.skip},
                                {"$limit": params.limit},
                                {"$count": "show_items"},
                            ],
                            "segments": [
                                {
                                    "$match": {
                                        "author": params.author,
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "customer",
                                        "localField": "author",
                                        "foreignField": "_id",
                                        "as": "author_details",
                                    }
                                },
                                {"$unwind": "$author_details"},
                                {
                                    "$project": {
                                        "author": 0,
                                        "filter": 0,
                                        "applied_filters": 0,
                                    }
                                },
                                {"$skip": params.skip},
                                {"$limit": params.limit},
                                {
                                    "$sort": {
                                        f"{column_target }": order,
                                        "_id": 1,
                                    }
                                },
                            ],
                        }
                    },
                ]
            )
        elif params.author == "" and params.tag != "":
            tags = params.tag.replace("[", "").replace("]", "").split(",")

            r = self.segments.aggregate(
                [
                    {
                        "$facet": {
                            "total_items": [
                                {
                                    "$match": {
                                        "tags": {"$in": tags},
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "customer",
                                        "localField": "author",
                                        "foreignField": "_id",
                                        "as": "author_details",
                                    }
                                },
                                {"$unwind": "$author_details"},
                                {
                                    "$project": {
                                        "author": 0,
                                        "filter": 0,
                                        "applied_filters": 0,
                                    }
                                },
                                {"$count": "total_items"},
                            ],
                            "total_show": [
                                {
                                    "$match": {
                                        "tags": {"$in": tags},
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "customer",
                                        "localField": "author",
                                        "foreignField": "_id",
                                        "as": "author_details",
                                    }
                                },
                                {"$unwind": "$author_details"},
                                {
                                    "$project": {
                                        "author": 0,
                                        "filter": 0,
                                        "applied_filters": 0,
                                    }
                                },
                                {"$skip": params.skip},
                                {"$limit": params.limit},
                                {"$count": "show_items"},
                            ],
                            "segments": [
                                {
                                    "$match": {
                                        "tags": {"$in": tags},
                                    }
                                },
                                {
                                    "$lookup": {
                                        "from": "customer",
                                        "localField": "author",
                                        "foreignField": "_id",
                                        "as": "author_details",
                                    }
                                },
                                {"$unwind": "$author_details"},
                                {
                                    "$project": {
                                        "author": 0,
                                        "filter": 0,
                                        "applied_filters": 0,
                                    }
                                },
                                {"$skip": params.skip},
                                {"$limit": params.limit},
                                {
                                    "$sort": {
                                        f"{column_target }": order,
                                        "_id": 1,
                                    }
                                },
                            ],
                        }
                    },
                ]
            )

        resp = []
        if r != None:
            for item in await r.to_list(
                length=params.limit
            ):  # por variar y provar ( mas eficiente)
                resp = item
            # print(resp)

        return resp

    async def get_all_author_in_segments(self) -> AuthorsInSegments:

        final_response = {}
        authors = self.segments.aggregate(
            [
                {
                    "$facet": {
                        "authors": [
                            {
                                "$lookup": {
                                    "from": "customer",
                                    "localField": "author",
                                    "foreignField": "_id",
                                    "as": "author_details",
                                }
                            },
                            {"$unwind": "$author_details"},
                            {
                                "$project": {
                                    "author_details.name": 1,
                                    "author": 1,
                                    "_id": 0,
                                }
                            },
                        ]
                    }
                },
            ]
        )

        resp = []

        if authors != None:
            for item in await authors.to_list(length=None):
                resp = item  # en este caso no importa ya que siempre devolvera un unico objeto

            list_authors = []
            temp_list = []

            for x in resp["authors"]:
                if x["author"] not in temp_list:
                    temp_list.append(x["author"])
                    list_authors.append(
                        dict(id=x["author"], name=x["author_details"]["name"])
                    )
            final_response["authors"] = list_authors

        return final_response

    async def facet_test(self) -> Any:
        # r = self.clients_customer.aggregate(
        #     [
        #         {
        #             "$facet": {
        #                 "items": [
        #                     {"$match": {"blacklist_status": False}},
        #                 ],
        #             },
        #         },
        #         {"$unwind": "$items"},
        #         {"$match": {"items.civil_status": "single"}},
        #         {
        #             "$facet": {
        #                 "result": [
        #                     {"$match": {"items.age": 77}},
        #                 ],
        #             }
        #         },
        #     ]
        # )

        r = self.clients_customer.aggregate(
            [
                {"$match": {"civil_status": "single"}},
                # {"$match": {"email.isMain": True, "email.email": "t23@hotmal.com"}},
                # {"$match": {"age": 77}},
            ],
            allowDiskUse=True,
        )
        resp = []
        if r != None:
            for item in await r.to_list(
                length=None
            ):  # por variar y provar ( mas eficiente)
                resp.append(item)

        # print(resp)

        return resp
