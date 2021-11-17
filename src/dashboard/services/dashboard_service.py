import statistics
from functools import reduce
from datetime import datetime, timedelta
from collections import Counter

from fastapi import status
from fastapi.responses import JSONResponse

from src.dashboard.schemas.response.dashboard import (
    DashBoardActivity,
    DashBoardDemographics,
    PmsGeneral,
    Forecasts,
)

from src.dashboard.repository import PmsQueries
from core.libs import pms_lib
from http_exceptions import NotFoundException


class DashBoardService(PmsQueries):
    """
    Service to get PMS usage statistics

    """

    def __init__(self):
        super().__init__()

    def revenue_per_stay(self, date_from: str, date_to: str, property: str):
        revenues_booker = self.get_revenues("pms_booker")
        revenues_guest = self.get_revenues("pms_pri_guest")

        joined_list = revenues_booker + revenues_guest

        print(joined_list)

    async def get_dashboard_graphs(self, customer_id, sensor):
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
        lodges_list = []
        upselling_list = []
        forecasts_list = []
        forecasts_list_reduced = []

        try:

            customer_reservations_master = self.get_all_customer_stays(customer_id)

            # ESTADIA PROMEDIO
            async for reservation in customer_reservations_master:
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

                async for i in self.get_upsellings_food_beverages(
                    customer_id, reservation["entity"]
                ):
                    upselling_list.append(i)

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

                        pax_list.append(
                            book["adults"] + book["children"] + book["babies"]
                        )

                    async for room_type in self.group_by_most_used_roomType(
                        customer_id, reservation["entity"]
                    ):
                        used_room_type_list.append(room_type)

                    async for cancellation in self.get_cancellations(
                        customer_id, reservation["entity"]
                    ):
                        if cancellation["_id"] == "cancelled":
                            cancellation_list.append(cancellation)

                    async for channel in self.get_preferred_sale_channel(customer_id):
                        sales_channels_list.append(channel)

                    # RESUMEN GLOBAL

                    lodges_list.append(
                        PmsGeneral(
                            first_checkin=datetime.strptime(
                                reservation["data"]["bBooks"][0]["checkin"], "%Y-%m-%d"
                            ),
                            first_checkout=datetime.strptime(
                                reservation["data"]["bBooks"][0]["checkout"], "%Y-%m-%d"
                            ),
                            first_property=reservation["data"]["sproperty"]["name"],
                            first_room_type=reservation["data"]["bBooks"][0][
                                "riRoomType"
                            ]["name"],
                            first_amount=reservation["data"]["bBooks"][0]["netAmt"],
                            last_checkin=datetime.strptime(
                                reservation["data"]["bBooks"][-1]["checkin"], "%Y-%m-%d"
                            ),
                            last_checkout=datetime.strptime(
                                reservation["data"]["bBooks"][-1]["checkout"],
                                "%Y-%m-%d",
                            ),
                            last_property=reservation["data"]["sproperty"]["name"],
                            last_room_type=reservation["data"]["bBooks"][-1][
                                "riRoomType"
                            ]["name"],
                            last_amount=reservation["data"]["bBooks"][-1]["netAmt"],
                            first_duration=(
                                datetime.strptime(
                                    reservation["data"]["bBooks"][0]["checkout"],
                                    "%Y-%m-%d",
                                )
                                - datetime.strptime(
                                    reservation["data"]["bBooks"][0]["checkin"],
                                    "%Y-%m-%d",
                                )
                            )
                            / timedelta(milliseconds=1),
                            last_duration=(
                                datetime.strptime(
                                    reservation["data"]["bBooks"][-1]["checkout"],
                                    "%Y-%m-%d",
                                )
                                - datetime.strptime(
                                    reservation["data"]["bBooks"][-1]["checkin"],
                                    "%Y-%m-%d",
                                )
                            )
                            / timedelta(milliseconds=1),
                        )
                    )

                elif reservation["entity"] == "pms_pri_guest":
                    incomes_list.append(reservation["data"]["netAmt"])
                    nights_list.append(reservation["data"]["nights"])

                    checkout_date = datetime.strptime(
                        reservation["data"]["checkout"], "%Y-%m-%d"
                    )
                    checkin_date = datetime.strptime(
                        reservation["data"]["checkin"], "%Y-%m-%d"
                    )

                    stay_time = (checkout_date - checkin_date) / timedelta(
                        milliseconds=1
                    )
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
                        if cancellation["_id"] == "cancelled":
                            cancellation_list.append(cancellation)

                    # RESUMEN GLOBAL

                    lodges_list.append(
                        PmsGeneral(
                            first_checkin=datetime.strptime(
                                reservation["data"]["checkin"], "%Y-%m-%d"
                            ),
                            first_checkout=datetime.strptime(
                                reservation["data"]["checkout"], "%Y-%m-%d"
                            ),
                            first_property=reservation["data"]["riRatePlan"][
                                "sproperty"
                            ]["name"],
                            first_room_type=reservation["data"]["riRoomType"]["name"],
                            first_amount=reservation["data"]["netAmt"],
                            last_checkin=datetime.strptime(
                                reservation["data"]["checkin"], "%Y-%m-%d"
                            ),
                            last_checkout=datetime.strptime(
                                reservation["data"]["checkout"], "%Y-%m-%d"
                            ),
                            last_property=reservation["data"]["riRatePlan"][
                                "sproperty"
                            ]["name"],
                            last_room_type=reservation["data"]["riRoomType"]["name"],
                            last_amount=reservation["data"]["netAmt"],
                            first_duration=(
                                datetime.strptime(
                                    reservation["data"]["checkout"], "%Y-%m-%d"
                                )
                                - datetime.strptime(
                                    reservation["data"]["checkin"], "%Y-%m-%d"
                                )
                            )
                            / timedelta(milliseconds=1),
                            last_duration=(
                                datetime.strptime(
                                    reservation["data"]["checkout"], "%Y-%m-%d"
                                )
                                - datetime.strptime(
                                    reservation["data"]["checkin"], "%Y-%m-%d"
                                )
                            )
                            / timedelta(milliseconds=1),
                        )
                    )

            upselling_food_beverages = pms_lib.remove_duplicates(upselling_list)

            [
                forecasts_list.append(
                    Forecasts(
                        concept=item["_id"],
                        count=item["count"],
                        net_amount=item["total_income"],
                        avg_income=item["average_income"],
                    )
                )
                for item in upselling_food_beverages
            ]

            [forecasts_list_reduced.append(i.dict()) for i in forecasts_list]

            response = {
                "pms_response": {"status_code": status.HTTP_200_OK, "message": "Ok"},
                "pms_first_stay": {
                    "date": lodges_list[0].first_checkin.strftime("%Y-%m-%d"),
                    "property": lodges_list[0].first_property,
                    "duration": int(lodges_list[0].first_duration),
                    "room_type": lodges_list[0].first_room_type,
                    "upselling": pms_lib.get_revenues(
                        forecasts_list_reduced, "UPSELLING"
                    )["count"],
                    "amount": lodges_list[0].first_amount,
                },
                "pms_last_stay": {
                    "date": lodges_list[-1].last_checkin.strftime("%Y-%m-%d"),
                    "property": lodges_list[-1].last_property,
                    "duration": int(lodges_list[-1].last_duration),
                    "room_type": lodges_list[-1].last_room_type,
                    "upselling": pms_lib.get_revenues(
                        forecasts_list_reduced, "UPSELLING"
                    )["count"],
                    "amount": lodges_list[-1].last_amount,
                },
                "pms_avg_stay": int(statistics.mean(stay_time_list)),
                "pms_last_used_room_type": lodges_list[-1].last_room_type,
                "pms_most_used_room_type": pms_lib.validate_most_used_room_type(
                    used_room_type_list
                ),
                "pms_total_income": pms_lib.get_revenues(
                    forecasts_list_reduced, "ACCOMMODATION"
                )["total"]
                + pms_lib.get_revenues(forecasts_list_reduced, "UPSELLING")["total"]
                + pms_lib.get_revenues(forecasts_list_reduced, "FOOD AND BEVERAGES")[
                    "total"
                ],
                # "pms_total_income": reduce(lambda a, b: a + b, incomes_list),
                "pms_avg_pax": int(statistics.mean(pax_list)),
                "pms_consolidate_nights": int(reduce(lambda a, b: a + b, nights_list)),
                "pms_avg_anticipation": int(statistics.mean(anticipation_list)),
                "pms_cancelled_bookings": cancellation_list[0]["count"]
                if len(cancellation_list) > 0
                else 0,
                "pms_preferred_sales_channel": sales_channels_list[0]["_id"]
                if len(sales_channels_list) > 0
                else "None",
                "pms_total_lodge_income": pms_lib.get_revenues(
                    forecasts_list_reduced, "ACCOMMODATION"
                )["total"],
                "pms_total_upsellings": pms_lib.get_revenues(
                    forecasts_list_reduced, "UPSELLING"
                )["count"],
                "pms_total_upsellings_income": pms_lib.get_revenues(
                    forecasts_list_reduced, "UPSELLING"
                )["total"],
                "pms_food_beverages_paid_total": pms_lib.get_revenues(
                    forecasts_list_reduced, "FOOD AND BEVERAGES"
                )["total"],
                "pms_food_beverages_consuptions": pms_lib.get_revenues(
                    forecasts_list_reduced, "FOOD AND BEVERAGES"
                )["count"],
                "pms_food_beverages_avg_cons_expenses": pms_lib.get_revenues(
                    forecasts_list_reduced, "FOOD AND BEVERAGES"
                )["avg"],
                "pms_lodges_per_year": {
                    "years": pms_lib.get_lodges_per_year(lodges_list)["years"],
                    "lodges": pms_lib.get_lodges_per_year(lodges_list)["ocurrences"],
                },
            }

            return response
        except Exception:
            response = {
                "code": status.HTTP_404_NOT_FOUND,
                "message": f"Customer doesn't have interaction with this sensor",
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
