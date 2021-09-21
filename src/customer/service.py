import json

from .repository import MongoQueries

from .schemas import (
    SearchCustomersQueryParams,
    SearchCustomersResponse,
    CustomerProfileHeaderResponse,
    CustomerProfileDetailResponse,
    CustomerLogBook,
    CustomerMarketingSubscriptions,
    SearchCustomers,
    CustomerNotesAndcomments,
    NotesAndCommentsResponse,
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
                print("F :(")

        # response = self.build_response(customers, total_customer)

        return self.build_response_search(customers, total_customer)

    def build_response_search(self, list_items, total_customer):

        finalresponse = {
            "customers": list_items,
            "total_items": total_customer,
            "total_show": len(list_items),
        }
        return SearchCustomersResponse(**finalresponse)

    def get_customer_notes_comments(self, customer_id: int) -> CustomerNotesAndcomments:

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

    def get_profile_header(self, customer_id: int) -> CustomerProfileHeaderResponse:
        data = {
            "id_": "djfaklsdf",
            "name": "john",
            "score": 50,
            "languages": ["ENG", "SPANISH"],
            "country": "VEN",
            "membership": "?",
            "gender": "NO BINARY KEK",
            "age": 36,
            "next_hotel_stay": "random hotel",
            "next_stay_date": "25/10/2021",
            "last_checkout_date": "21/04/2021",
            "last_stay_hotel": "super random hotel",
            "total_stays": 1,
            "days_since_last_stay": 15,
            "lifetime_expenses": 680.60,
            "total_lodging_expenses": 350.98,
            "miscellaneous_expenses": 329.62,
            "average_expenditure_per_stay": 680.60,
            "average_days_before_booking": 35,
        }

        return CustomerProfileHeaderResponse(**data)

    def get_profile_details(self, customer_id: int) -> CustomerProfileDetailResponse:
        data = {
            "most_visited_hotel": "random hotel",
            "recency": "?",
            "email": "mail@correo.com",
            "phone": "00000000000",
            "social_networks": [
                {"name": "Instagram", "username": "@randomuser"},
                {"name": "Facebook", "username": "@randomuserfacebook"},
            ],
            "accepted_terms": [
                {
                    "document_url": "http://google.co.ve",
                    "name": "Terminos 2021",
                    "description": "Terminos actualizados sobre el uso de nuestros servicios",
                }
            ],
            "interests": ["Basketball", "Chess", "CSGO"],
            "communication_methods": {
                "email": {"sent": 125, "opened": 15},
                "hostpod": {"ads_viewed": 16},
                "sms": {"sent_sms": 514},
                "signage": {"ads_sent": 100, "used_devices": 4},
                "butler": {"ads_sent": 16},
            },
        }

        return CustomerProfileDetailResponse(**data)

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

    def get_customer_marketing_subscriptions(self, customer_id):
        data = {
            "emails": [
                {"email": "test@email.com", "subscribed": False, "is_primary": True},
                {"email": "anotherTest@email.com", "subscribed": True},
            ],
            "devices": [
                {
                    "mac_address": "00:00:00:00:00:01",
                    "subscribed": False,
                },
                {
                    "mac_address": "00:00:00:00:00:02",
                    "subscribed": True,
                },
            ],
            "phones": [
                {
                    "phone_iso_code": "+58",
                    "phone": "4144964508",
                    "is_primary": True,
                    "subscribed": False,
                },
                {"phone_iso_code": "+1", "phone": "4457988", "subscribed": False},
            ],
        }

        return CustomerMarketingSubscriptions(**data)

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
