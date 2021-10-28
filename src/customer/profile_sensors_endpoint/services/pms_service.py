import statistics
import functools
from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import status
from fastapi.responses import JSONResponse

from ..schemas.response.customers_sensors import (
    PmsBooking,
    PmsResponse,
    PmsHistory,
    PmsHistoryData,
)
from src.customer.profile_sensors_endpoint.repository.pms import PmsQueries


class PmsService(PmsQueries):
    """
    Service to get PMS usage statistics

    """

    def __init__(self):
        super().__init__()

    def get_bookings(self, customer_id):
        pass

    async def get_pms_stats(self, customer_id, sensor):
        masters_list = []
        books_list = []
        stay_time_list = []
        used_room_type_list = []
        incomes_list = []
        nights_list = []
        anticipation_list = []
        cancellation_list = []
        sales_channels_list = []

        try:

            customer_reservations = self.get_all_customer_stays(customer_id)

            # ESTADIA PROMEDIO
            async for master in customer_reservations:
                masters_list.append(master)

            for master in masters_list:
                master_reservation_creation_date = datetime.strptime(
                    master["data"]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
                master_reservation_checkin_date = datetime.strptime(
                    master["data"]["checkin"], "%Y-%m-%d"
                )
                anticipation_time = (
                    master_reservation_checkin_date - master_reservation_creation_date
                )
                anticipation_list.append(anticipation_time.days)

                for book in master["data"]["bBooks"]:
                    books_list.append(book)
                    incomes_list.append(book["netAmt"])
                    nights_list.append(book["nights"])

                    checkout_date = datetime.strptime(book["checkout"], "%Y-%m-%d")
                    checkin_date = datetime.strptime(book["checkin"], "%Y-%m-%d")

                    stay_time = checkout_date - checkin_date
                    stay_time_list.append(stay_time.days)

            async for type in self.group_by_most_used_roomType(customer_id):
                used_room_type_list.append(type)

            async for cancellation in self.get_cancellations(customer_id):
                if cancellation["_id"][0] == "cancelled":
                    cancellation_list.append(cancellation)

            async for channel in self.get_preferred_sale_channel(customer_id):
                sales_channels_list.append(channel)

            # RESUMEN GLOBAL

            first_lodge_checkin = datetime.strptime(
                masters_list[0]["data"]["bBooks"][0]["checkin"], "%Y-%m-%d"
            )
            first_lodge_checkout = datetime.strptime(
                masters_list[0]["data"]["bBooks"][0]["checkout"], "%Y-%m-%d"
            )
            first_lodge_property = masters_list[0]["data"]["sproperty"]["code"]
            first_lodge_Room_type = masters_list[0]["data"]["bBooks"][0]["riRoomType"][
                "name"
            ]
            first_lodge_amount = masters_list[0]["data"]["bBooks"][0]["netAmt"]

            last_lodge_checkin = datetime.strptime(
                masters_list[-1]["data"]["bBooks"][-1]["checkin"], "%Y-%m-%d"
            )
            last_lodge_checkout = datetime.strptime(
                masters_list[-1]["data"]["bBooks"][-1]["checkout"], "%Y-%m-%d"
            )
            last_lodge_property = masters_list[-1]["data"]["sproperty"]["code"]
            last_lodge_Room_type = masters_list[-1]["data"]["bBooks"][-1]["riRoomType"][
                "name"
            ]
            last_lodge_amount = masters_list[-1]["data"]["bBooks"][-1]["netAmt"]

            first_lodge_duration = round(
                (first_lodge_checkout - first_lodge_checkin) / timedelta(days=1), 2
            )
            last_lodge_duration = round(
                (last_lodge_checkout - last_lodge_checkin) / timedelta(days=1), 2
            )

            response = {
                "pms_response": {"status_code": status.HTTP_200_OK, "message": "Ok"},
                "pms_first_stay": {
                    "date": first_lodge_checkin.strftime("%Y-%m-%d"),
                    "property": first_lodge_property,
                    "duration": first_lodge_duration,
                    "room_type": first_lodge_Room_type,
                    "amount": first_lodge_amount,
                },
                "pms_last_stay": {
                    "date": last_lodge_checkin.strftime("%Y-%m-%d"),
                    "property": last_lodge_property,
                    "duration": last_lodge_duration,
                    "room_type": last_lodge_Room_type,
                    "amount": last_lodge_amount,
                },
                "pms_avg_stay": round(statistics.mean(stay_time_list), 2),
                "pms_last_used_room_type": last_lodge_Room_type,
                "pms_most_used_room_type": used_room_type_list[0]["_id"][0],
                "pms_total_income": functools.reduce(lambda a, b: a + b, incomes_list),
                "pms_avg_pax": 0,
                "pms_consolidate_nights": functools.reduce(
                    lambda a, b: a + b, nights_list
                ),
                "pms_avg_anticipation": round(statistics.mean(anticipation_list), 2),
                "pms_cancelled_bookings": cancellation_list[0]["count"]
                if len(cancellation_list) > 0
                else 0,
                "pms_preferred_sales_channel": sales_channels_list[0]["_id"],
            }

            return response
        except:
            response = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": f"Customer doesn't have interaction with this sensor",
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)

    async def get_pms_history(self, customer_id, constrain, search, skip, limit):
        try:
            master_books_list = []
            single_books_list = []
            pms_history_list = []

            master = self.get_bookings_agg_customer(
                customer_id, constrain, search, skip, limit
            )

            async for book in master:
                master_books_list.append(book)

            for master in master_books_list:
                for book in master["data"]["bBooks"]:
                    single_books_list.append(book)

            for master in master_books_list:
                pms_history_list.append(
                    PmsHistoryData(
                        code=master["data"]["code"],
                        name=master["data"]["pguest"]["name"],
                        last_name=master["data"]["pguest"]["lastname"],
                        nationality=master["data"]["pguest"]["coreCountry"]["name"],
                        phone=master["pms_customer"][0]["phone"][0]["phone"],
                        address=master["pms_customer"][0]["address"],
                        email=master["data"]["pguest"]["email"],
                        documentId=[
                            {
                                "documentType": "DNI",
                                "documentNumber": master["data"]["pguest"]["dni"],
                            },
                            {
                                "documentType": "Passport",
                                "documentNumber": master["data"]["pguest"]["passport"],
                            },
                        ],
                        civil_status=master["pms_customer"][0]["civil_status"],
                        languages=master["pms_customer"][0]["email"][0]["email"],
                        country=master["data"]["pguest"]["coreCountry"]["name"],
                        city=master["pms_customer"][0]["city"],
                        booking={
                            "pms_book_code": master["data"]["bBooks"][0]["code"],
                            "pms_book_checkin": master["data"]["bBooks"][0]["checkin"],
                            "pms_book_checkout": master["data"]["bBooks"][0][
                                "checkout"
                            ],
                            "pms_book_cost": 0,
                            "pms_book_room_type": "#PENDIENTE",
                            "pms_book_rate_plat": "#PENDIENTE",
                            "pms_book_currency": "#PENDIENTE",
                            "pms_book_reseller": "#PENDIENTE",
                            "pms_book_meal_plan": "#PENDIENTE",
                            "pms_book_property": "#PENDIENTE",
                            "pms_book_taxes": "#PENDIENTE",
                        },
                    )
                )
            response = {
                "pms_history_response": {
                    "status_code": status.HTTP_200_OK,
                    "message": "Ok",
                },
                "id": customer_id,
                "total_items": 0,
                "showing": limit,
                "skip": skip,
                "booking_history_data": pms_history_list,
            }

            if len(pms_history_list) > 0:
                return response
            else:
                response = {
                    "code": status.HTTP_404_NOT_FOUND,
                    "message": f"Not Found",
                }
                return JSONResponse(
                    status_code=status.HTTP_404_NOT_FOUND, content=response
                )
        except Exception as err:
            response = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": f"Error: {err}",
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
