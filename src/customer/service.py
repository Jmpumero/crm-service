from typing import Any
from src.customer.schemas import get
from src.customer.schemas.get import responses
from src.customer.schemas.get.query_params import SegmenterQueryParams
from src.customer.schemas.get.responses import customers
from src.customer.schemas.get.responses import blacklist
from src.customer.schemas.get.responses.customer_crud import (
    SearchMerge,
    SearchMergeResponse,
)
from src.customer.schemas.get.responses.segmenter import AuthorsInSegments, Segmenter

from .repository import MongoQueries
import json
from .repository import MongoQueries
from src.customer.repositories import HistorySensorQueries
from .schemas import (
    SearchCustomersQueryParams,
    SearchCustomersResponse,
    CustomerLogBook,
    SearchCustomers,
    CustomerNotesAndcomments,
    NotesAndCommentsResponse,
    BlacklistCustomersResponse,
    SensorHistoryResponse,
    BlacklistCustomer,
    BlacklistQueryParams,
    CustomerQueryParamsSensor,
    BlackListBody,
    CreateCustomerBody,
    SearchUpdateResponse,
    SearchUpdate,
    SearchCrudQueryParams,
    CustomerCRUDResponse,
    SensorHistoryResponse,
    UpdateCustomerBody,
    BlackListBodyResponse,
    CrossSelling,
    CrossSellingQueryParams,
    NewCrossSelling,
    Product,
    CrossSellingCreatedResponse,
    CrossSellingAndProductsResponse,
    Segmenter,
)


class Service(MongoQueries):
    def __init__(self) -> None:
        super().__init__()

    async def get_customers(
        self, query_params: SearchCustomersQueryParams
    ) -> SearchCustomersResponse:

        customers = []
        cursor = None
        total_customer = await self.total_customer()
        customer = None

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
                    # print(customer)

                    customers.append(customer)

        else:
            if query_params.column_name.replace(" ", "") and query_params.contain != "":

                cursor = self.filter_search_customers(
                    query_params.contain,
                    query_params.query,
                    query_params.column_name.replace(" ", "").lower(),
                    query_params.skip,
                    query_params.limit,
                    query_params.order,
                    query_params.column_order,
                )
                if cursor != None:

                    for customer in await cursor.to_list(length=None):

                        # print(customer)
                        # customers.append(SearchCustomers(**customer))
                        customers.append(customer)

            else:
                print("Caso no valido error ")

        if customer != None:

            return SearchCustomersResponse(**customer)
        else:
            resp = {}
            resp["items"] = []
            resp["total_items"] = 0
            return resp

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
                    "source": "PMS",
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
    ) -> BlacklistCustomersResponse:
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

    async def get_history_sensor(
        self, customer_id, query_params: CustomerQueryParamsSensor
    ):
        data_s = []
        total = 2
        if query_params.sensor == "sensor_1":

            r = await HistorySensorQueries.get_customer_sensor_1(self, customer_id)
            pass
        elif query_params.sensor == "sensor_2":
            pass
        elif query_params.sensor == "sensor_3":
            pass
        elif query_params.sensor == "sensor_4":
            pass

        data_s = [
            {"date": "25-10-2020 15:00", "property": "HPA", "duration": "30min"},
            {"date": "15-06-2020 16:50", "property": "H Barcelona", "duration": "1h"},
        ]

        response = {
            "sensor_data": data_s,
            "total_items": total,
            "total_show": len(data_s),
        }

        return r

    async def post_blacklist_update_customer(self, body: BlackListBody):

        return await self.update_customer_in_blacklist(body)

    async def post_create_customer(self, body: CreateCustomerBody):

        return await self.insert_one_customer(body)

    async def get_all_customer_with_blacklist(
        self, query_params: SearchCrudQueryParams
    ) -> SearchUpdateResponse:
        customers = []
        special_query = {}
        special_query["customer_status"] = True
        special_query["blacklist_status"] = False
        cursor = None
        total_customer = await self.total_customer()

        if query_params.query == "":

            cursor = self.find_all_customers_in_crud_view(
                query_params.skip,
                query_params.limit,
                query_params.column_sort.replace(" ", ""),
                query_params.order,
                special_query,
            )

        else:

            cursor = self.find_filter_customers_in_crud_view(
                query_params.query,
                query_params.skip,
                query_params.limit,
                query_params.column_sort.replace(" ", ""),
                query_params.order,
            )

        for customer in await cursor.to_list(length=None):
            # print(customer)
            customers.append(SearchUpdate(**customer))

        response = {
            "customers": customers,
            "total_items": total_customer,
            "total_show": len(customers),
        }
        return SearchUpdateResponse(**response)

    async def update_customer(self, body) -> CustomerCRUDResponse:
        response = None
        response = await self.update_customer_(body)

        return CustomerCRUDResponse(**response)

    async def delete_customer(self, customer_id) -> CustomerCRUDResponse:
        response = None
        response = await self.delete_one_customer(customer_id)

        if response != None:
            response = {"msg": " Success Customer deleted ", "code": 204}
        else:
            response = {
                "msg": " Failed Customer Delete, Customer not found ",
                "code": 404,
            }
        return CustomerCRUDResponse(**response)

    async def merger_customers_with_update(self, body) -> CustomerCRUDResponse:
        response = None
        response = await self.merge_customers(body)
        return CustomerCRUDResponse(**response)

    async def post_create_cross_selling_product(
        self, body: Product
    ) -> CrossSellingCreatedResponse:

        return await self.insert_one_cross_selling_product(body)

    async def post_create_cross_selling(
        self, body: NewCrossSelling
    ) -> CrossSellingCreatedResponse:

        return await self.insert_many_cross_selling(body)

    async def get_product_and_cross_selling_items(
        self,
        query_params,
    ) -> CrossSellingAndProductsResponse:
        response = {}
        total_cross_selling = 0
        items_cross_selling = []
        items_product = []

        cursor_cross_selling = await self.get_all_cross_selling(query_params)
        cursor_products = await self.get_all_products()
        total_cross_selling = await self.get_total_cross_selling()

        for item in await cursor_cross_selling.to_list(length=None):
            items_cross_selling.append(CrossSelling(**item))

        for product in await cursor_products.to_list(length=None):
            items_product.append(Product(**product))

        response = {
            "products": items_product,
            "cross_selling": items_cross_selling,
            "total_cross_selling_items": total_cross_selling,
            "total_cross_selling_show": len(items_cross_selling),
        }
        return CrossSellingAndProductsResponse(**response)

    async def get_segmenters(self, query_params: SegmenterQueryParams) -> Any:

        segments = None

        segments = await self.find_segments(query_params)
        segments["global_total_clients"] = await self.total_customer()
        segments["total_enable_clients"] = (
            await self.total_customer()
        ) - await self.total_customer_in_blacklist(True)
        return segments

    async def get_author_segments_list(self) -> AuthorsInSegments:
        authors = await self.get_all_author_in_segments()

        return authors

    async def get_test(self) -> Any:

        r = await self.facet_test()
        return r
