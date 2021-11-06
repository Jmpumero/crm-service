import statistics
import functools
from datetime import datetime, timedelta
from fastapi import status
from fastapi.responses import JSONResponse

from ..schemas.response.customers_sensors import (
    PmsBook,
    PmsHistoryGuest,
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
        pax_list = []

        # try:

        customer_reservations = self.get_all_customer_stays(customer_id)

        # ESTADIA PROMEDIO
        async for reservation in customer_reservations:
            masters_list.append(reservation)

        for reservation in masters_list:

            master_reservation_creation_date = datetime.strptime(
                reservation["data"]["createdAt"], "%Y-%m-%dT%H:%M:%S.%fZ"
            )
            master_reservation_checkin_date = datetime.strptime(
                reservation["data"]["checkin"], "%Y-%m-%d"
            )
            anticipation_time = (
                master_reservation_creation_date - master_reservation_checkin_date
            ) / timedelta(milliseconds=1)
            anticipation_list.append(anticipation_time)

            if reservation["entity"] == "pms_booker":
                for book in reservation["data"]["bBooks"]:
                    books_list.append(book)
                    incomes_list.append(book["netAmt"])
                    nights_list.append(book["nights"])

                    checkout_date = datetime.strptime(book["checkout"], "%Y-%m-%d")
                    checkin_date = datetime.strptime(book["checkin"], "%Y-%m-%d")

                    stay_time = (checkout_date - checkin_date) / timedelta(
                        milliseconds=1
                    )
                    stay_time_list.append(stay_time)

                    pax_list.append(book["adults"] + book["children"] + book["babies"])

                async for room_type in self.group_by_most_used_roomType(
                    customer_id, reservation["entity"]
                ):
                    used_room_type_list.append(room_type)

                async for cancellation in self.get_cancellations(
                    customer_id, reservation["entity"]
                ):
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
                first_lodge_property = masters_list[0]["data"]["sproperty"]["name"]
                first_lodge_Room_type = masters_list[0]["data"]["bBooks"][0][
                    "riRoomType"
                ]["name"]
                first_lodge_amount = masters_list[0]["data"]["bBooks"][0]["netAmt"]

                last_lodge_checkin = datetime.strptime(
                    masters_list[-1]["data"]["bBooks"][-1]["checkin"], "%Y-%m-%d"
                )
                last_lodge_checkout = datetime.strptime(
                    masters_list[-1]["data"]["bBooks"][-1]["checkout"], "%Y-%m-%d"
                )
                last_lodge_property = masters_list[-1]["data"]["sproperty"]["name"]
                last_lodge_Room_type = masters_list[-1]["data"]["bBooks"][-1][
                    "riRoomType"
                ]["name"]
                last_lodge_amount = masters_list[-1]["data"]["bBooks"][-1]["netAmt"]

                first_lodge_duration = (
                    first_lodge_checkout - first_lodge_checkin
                ) / timedelta(milliseconds=1)
                last_lodge_duration = (
                    last_lodge_checkout - last_lodge_checkin
                ) / timedelta(milliseconds=1)

            elif reservation["entity"] == "pms_pri_guest":
                incomes_list.append(reservation["data"]["netAmt"])
                nights_list.append(reservation["data"]["nights"])

                checkout_date = datetime.strptime(
                    reservation["data"]["checkout"], "%Y-%m-%d"
                )
                checkin_date = datetime.strptime(
                    reservation["data"]["checkin"], "%Y-%m-%d"
                )

                stay_time = (checkout_date - checkin_date) / timedelta(milliseconds=1)
                stay_time_list.append(stay_time)

                pax_list.append(
                    reservation["data"]["adults"]
                    + reservation["data"]["children"]
                    + reservation["data"]["babies"]
                )

                async for room_type in self.group_by_most_used_roomType(
                    customer_id, reservation["entity"]
                ):
                    used_room_type_list.append(room_type)

                async for cancellation in self.get_cancellations(
                    customer_id, reservation["entity"]
                ):
                    if cancellation["_id"][0] == "cancelled":
                        cancellation_list.append(cancellation)

                # RESUMEN GLOBAL

                first_lodge_checkin = datetime.strptime(
                    masters_list[0]["data"]["checkin"], "%Y-%m-%d"
                )
                first_lodge_checkout = datetime.strptime(
                    masters_list[0]["data"]["checkout"], "%Y-%m-%d"
                )
                first_lodge_property = masters_list[0]["data"]["riRatePlan"][
                    "sproperty"
                ]["name"]
                first_lodge_Room_type = masters_list[0]["data"]["riRoomType"]["name"]
                first_lodge_amount = masters_list[0]["data"]["netAmt"]

                last_lodge_checkin = datetime.strptime(
                    masters_list[-1]["data"]["checkin"], "%Y-%m-%d"
                )
                last_lodge_checkout = datetime.strptime(
                    masters_list[-1]["data"]["checkout"], "%Y-%m-%d"
                )
                last_lodge_property = masters_list[-1]["data"]["riRatePlan"][
                    "sproperty"
                ]["name"]
                last_lodge_Room_type = masters_list[-1]["data"]["riRoomType"]["name"]
                last_lodge_amount = masters_list[-1]["data"]["netAmt"]

                first_lodge_duration = (
                    first_lodge_checkout - first_lodge_checkin
                ) / timedelta(milliseconds=1)
                last_lodge_duration = (
                    last_lodge_checkout - last_lodge_checkin
                ) / timedelta(milliseconds=1)

        response = {
            "pms_response": {"status_code": status.HTTP_200_OK, "message": "Ok"},
            "pms_first_stay": {
                "date": first_lodge_checkin.strftime("%Y-%m-%d"),
                "property": first_lodge_property,
                "duration": int(first_lodge_duration),
                "room_type": first_lodge_Room_type,
                "amount": first_lodge_amount,
            },
            "pms_last_stay": {
                "date": last_lodge_checkin.strftime("%Y-%m-%d"),
                "property": last_lodge_property,
                "duration": int(last_lodge_duration),
                "room_type": last_lodge_Room_type,
                "amount": last_lodge_amount,
            },
            "pms_avg_stay": int(statistics.mean(stay_time_list)),
            "pms_last_used_room_type": last_lodge_Room_type,
            "pms_most_used_room_type": used_room_type_list[0]["_id"][0],
            "pms_total_income": functools.reduce(lambda a, b: a + b, incomes_list),
            "pms_avg_pax": int(statistics.mean(pax_list)),
            "pms_consolidate_nights": int(
                functools.reduce(lambda a, b: a + b, nights_list)
            ),
            "pms_avg_anticipation": -int(statistics.mean(anticipation_list)),
            "pms_cancelled_bookings": cancellation_list[0]["count"]
            if len(cancellation_list) > 0
            else 0,
            "pms_preferred_sales_channel": sales_channels_list[0]["_id"]
            if len(sales_channels_list) > 0
            else "None",
        }

        return response
        # except Exception as err:
        #     response = {
        #         "code": status.HTTP_404_NOT_FOUND,
        #         "message": f"Customer doesn't have interaction with this sensor: {err}",
        #     }
        #     return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)

    async def get_pms_history(self, customer_id, constrain, search, skip, limit):
        # try:
        master_books_list = []
        pms_books_history_list = []
        pms_guests_history_list = []
        pms_companions_history_list = []

        master = self.get_bookings_agg_customer(
            customer_id, constrain, search, skip, limit
        )

        async for book in master:
            master_books_list.append(book)

        for master in master_books_list:
            for book in master["data"]["bBooks"]:
                pms_books_history_list.append(
                    PmsBook(
                        code=book["code"],
                        checkin=book["checkin"],
                        checkout=book["checkout"],
                        room_type=book["riRoomType"]["name"],
                        rate_plan=book["riRatePlan"]["name"],
                        reseller=master["data"]["preseller"]["name"],
                        meal_plan=book["riMealPlan"]["name"],
                        property=master["data"]["sproperty"]["name"],
                    )
                )
                for guest in book["bBookPGuests"]:
                    if guest["isMain"]:
                        pms_guests_history_list.append(
                            PmsHistoryGuest(
                                name=master["data"]["pguest"]["name"],
                                last_name=master["data"]["pguest"]["lastname"],
                                nationality="PENDIENTE",
                                phone=master["data"]["pguest"]["phone"],
                                # address=master["data"]["pms_customer"]["address"],
                                email=master["data"]["pguest"]["email"],
                                documentId=[
                                    {
                                        "documentType": "DNI",
                                        "documentNumber": master["data"]["pguest"][
                                            "dni"
                                        ],
                                    },
                                    {
                                        "documentType": "Passport",
                                        "documentNumber": master["data"]["pguest"][
                                            "passport"
                                        ],
                                    },
                                ],
                                # civil_status=master["data"]["pms_customer"][
                                #     "civil_ststus"
                                # ],
                                age=(
                                    datetime.today()
                                    - datetime.strptime(
                                        master["data"]["pguest"]["birthdate"],
                                        "%Y-%m-%d",
                                    )
                                )
                                / timedelta(days=365.2425),
                                language="PENDIENTE",
                                country=master["data"]["pguest"]["coreCountry"]["name"],
                                # city=master["data"]["pms_customer"]["city"],
                            )
                        )

                    else:
                        pms_companions_history_list.append(
                            PmsHistoryGuest(
                                name=guest["pguest"]["name"],
                                last_name=guest["pguest"]["lastname"],
                                documentId=[
                                    {
                                        "documentType": "DNI",
                                        "documentNumber": guest["pguest"]["dni"],
                                    },
                                    {
                                        "documentType": "Passport",
                                        "documentNumber": guest["pguest"]["passport"],
                                    },
                                ],
                                age=(
                                    datetime.utcnow()
                                    - datetime.strptime(
                                        guest["pguest"]["birthdate"], "%Y-%m-%d"
                                    )
                                )
                                / timedelta(days=365.2425),
                            )
                        )
        response = {
            "pms_history_response": {
                "status_code": status.HTTP_200_OK,
                "message": "Ok",
            },
            "total_items": len(pms_books_history_list),
            "showing": limit,
            "skip": skip,
            "guest_data": pms_guests_history_list,
            "companion_data": pms_companions_history_list,
            "booking_data": pms_books_history_list,
        }

        if len(pms_books_history_list) > 0:
            return response
        else:
            response = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": f"Not Found",
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
        # except Exception as err:
        #     response = {
        #         "code": status.HTTP_404_NOT_FOUND,
        #         "message": f"Error: {err}",
        #     }
        #     return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
