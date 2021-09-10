from .schemas import (
    SearchCustomersQueryParams,
    SearchCustomersResponse,
    CustomerProfileHeaderResponse,
    CustomerProfileDetailResponse,
    CustomerLogBook,
)


class Service:
    def get(
        self, query_params: SearchCustomersQueryParams
    ) -> list[SearchCustomersResponse]:
        data = [
            {
                "name": "elber",
                "last_name": "nava",
                "age": 15,
                "email": "dafd",
                "phone": "1234",
                "nationality": "us",
                "address": "aaa" "",
                "document_identification": "1234679800",
                "civl_status": "married",
            }
        ]
        response = []

        for elem in data:
            response.append(SearchCustomersResponse(**elem))

        return response

    def get_profile_header(self, customer_id: int) -> CustomerProfileHeaderResponse:
        data = {
            "id_": "djfaklsdf",
            "name": "john",
            "score": 50,
            "languages": ["ENG", "SPANISH"],
            "country": "VEN",
            "membership": "?",
            "gender": "NO BINARY",
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
