from typing import Any
from src.customer.schemas.get.responses import customers
from src.customer.schemas.get.responses import blacklist

from .repository import MongoQueries
import json

from .repository import MongoQueries

from .schemas import (
    SearchCustomersQueryParams,
    SearchCustomersResponse,
    CustomerLogBook,
    SearchCustomers,
    CustomerNotesAndcomments,
    NotesAndCommentsResponse,
    BlacklistCustomersResponse,
    BlacklistSensorResponse,
    BlacklistCustomer,
    BlacklistQueryParams,
    BlacklistQueryParamsSensor,
    BlackListBody,
)


import main


class Service(MongoQueries):
    def __init__(self) -> None:
        super().__init__()

    async def get_customers(
        self, query_params: SearchCustomersQueryParams
    ) -> list[SearchCustomers]:

        customers = []
        cursor = None
        total_customer = await self.total_customer()

        if query_params.query == "":
            if query_params.column_name:  # ultima validacion especial
                cursor = self.find_all_customers(
                    query_params.skip,
                    query_params.limit,
                    query_params.column_name.replace(" ", ""),
                    query_params.order,
                    query_params.column_order.replace(" ", ""),
                )

                for customer in await cursor.to_list(length=None):

                    customers.append(SearchCustomers(**customer))

        else:
            if query_params.column_name.replace(" ", ""):

                cursor = self.filter_search_customers(
                    query_params.contain,
                    query_params.query,
                    query_params.column_name.replace(" ", "").lower(),
                    query_params.skip,
                    query_params.limit,
                    query_params.order,
                    query_params.column_order,
                )
                if cursor:
                    for customer in await cursor.to_list(length=None):

                        # print(customer)
                        customers.append(SearchCustomers(**customer))

            else:
                print("Caso no valido error ")

        # response = self.build_response(customers, total_customer)

        return self.build_response_search(customers, total_customer)

    def build_response_search(self, list_items, total_customer):

        finalresponse = {
            "customers": list_items,
            "total_items": total_customer,
            "total_show": len(list_items),
        }
        return SearchCustomersResponse(**finalresponse)

    def get_customer_notes_comments(self, customer_id: str) -> CustomerNotesAndcomments:

        comments = []
        data = {
            "date": "18-12-2020",
            "comment": "Deseo la habitacion con una esfera del dragon",
            "created_by": "Huesped",
            "belong": "HPA",
        }
        data2 = {
            "date": "18-12-2020",
            "comment": "Deseo la habitacion con una temperatura ambiente",
            "created_by": "Huesped",
            "belong": "HPA",
        }
        comments.append(data)
        comments.append(data2)

        finalresponse = {
            "customer_comments": comments,
            "total_show": len(comments),
        }

        return NotesAndCommentsResponse(**finalresponse)

    def get_customer_logbook(self, customer_id) -> CustomerLogBook:
        data = {
            "first_contact_info": {
                "property_name": "random name",
                "insert_date": "21/08/2021",
                "updated": "21/08/2021",
            },
            "another_contacts": [
                {
                    "date": "22/02/2021",
                    "souce": "PMS",
                    "data": "random data",
                    "property_name": "HPA",
                },
                {
                    "date": "15/01/2021",
                    "souce": "CAST",
                    "data": "super random data",
                    "property_name": "",
                },
            ],
            "total_items": 56,
            "items_shown": 2,
        }

        return CustomerLogBook(**data)

    def build_blacklist_response(self, list_items, total):

        response = {
            "customers": list_items,
            "total_items": total,
            "total_show": len(list_items),
        }
        return BlacklistCustomersResponse(**response)

    async def get_customers_blacklist(
        self, query_params: BlacklistQueryParams
    ) -> list[BlacklistCustomer]:
        response = None
        customers = []
        cursor = None
        total = 0
        if query_params.query.replace(" ", "") != "":

            if query_params.query.lower() == "disable":
                total = await self.total_customer_in_blacklist(True)

            elif query_params.query.lower() == "enable":
                total = await self.total_customer_in_blacklist(False)

            else:
                print("valor de query errado")

            cursor = self.blacklist_search(
                query_params.query, query_params.skip, query_params.limit
            )

            if cursor != None:
                for customer in await cursor.to_list(length=None):
                    customers.append(BlacklistCustomer(**customer))
        else:
            print("el query no puede ser vacio")

        return self.build_blacklist_response(customers, total)

    def get_blacklist_sensor(
        self, customer_id, query_params: BlacklistQueryParamsSensor
    ):

        data_s = []
        total = 2
        if query_params.sensor == "sensor_1":
            pass
        elif query_params.sensor == "sensor_2":
            pass
        elif query_params.sensor == "sensor_3":
            pass
        elif query_params.sensor == "sensor_4":
            pass

        data_s = [
            {"fecha": "25-10-2020 15:00", "propiedad": "HPA", "duracion": "30min"},
            {"fecha": "15-06-2020 16:50", "propiedad": "H Barcelona", "duracion": "1h"},
        ]

        response = {
            "sensor_data": data_s,
            "total_items": total,
            "total_show": len(data_s),
        }

        return BlacklistSensorResponse(**response)

    async def post_blacklist_update_customer(self, body: BlackListBody):

        return await self.update_customer_in_blacklist(body)

    async def get_customer_sales_summary(self, customer_id):
        customer_in_redis = await main.app.state.redis_repo.get(str(customer_id))

        if not customer_in_redis:
            data = {
                "total_revenue": [
                    {"name": "upgrade_and_upselling", "quantity": 110},
                    {"name": "food_and_beverage", "quantity": 150},
                    {"name": "lodging", "quantity": 130},
                ],
                "frequent_visits": [
                    {"name": "superior king", "quantity": 4},
                    {"name": "king", "quantity": 2},
                    {"name": "double", "quantity": 2},
                ],
                "most_contracted_services": [
                    {"name": "extra key", "quantity": 118},
                    {"name": "tablet rental", "quantity": 112},
                    {"name": "spa access", "quantity": 220},
                    {"name": "bottle of wine", "quantity": 80},
                ],
                "check_ins": [
                    {"name": "complete", "quantity": 8},
                    {"name": "no complete", "quantity": 2},
                ],
                "most_visited_pages": [
                    {"name": "youtube", "quantity": 15},
                    {"name": "twitter", "quantity": 7},
                    {"name": "instagram", "quantity": 18},
                    {"name": "google", "quantity": 44},
                ],
                "use_of_suite_applications": [],
                "frequency_of_use_of_suite_applications": [
                    {"name": "cast", "quantity": 7},
                    {"name": "hostpod", "quantity": 11},
                ],
                "segment_where_it_is_located": [],
            }

            await main.app.state.redis_repo.set(str(customer_id), json.dumps(data))

            return data

        return json.loads(customer_in_redis)
