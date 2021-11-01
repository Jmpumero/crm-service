import statistics
from datetime import datetime, timedelta
from typing import Any, Optional

from fastapi import status
from fastapi.responses import JSONResponse

from ..schemas.response.customers_sensors import HistoryData, VisitedApps
from src.customer.profile_sensors_endpoint.repository.cast_hotspot import (
    CastHotSpotQueries,
)


class CastService(CastHotSpotQueries):
    """
    Service to get customer Cast usage statistics

    - Number of Customer Connections to Cast
    - Average Time of Customer Connection to Cast
    - All Visited Applications Data (Name, Visits)
    - Most Visited Application Data (Name, Visits, Average Visit Time)
    - Date of First Connection to Cast
    - Date of Last Connection to Cast
    - Most Used Device ID in DW
    - Last Cast Playback Data (Title, Duration, Playback Date)

    - List of Playbacks for te given Customer**
        - Playback Date
        - Used App,
        - Played Content
        - Playback Duration
        - Used Device

    """

    def __init__(self):
        super().__init__()

    async def get_cast_stats(self, customer_id: str, sensor: str) -> Any:
        try:
            connection_time_list = []
            playback_most_used_app_list = []
            playback_used_apps_list = []
            most_used_device_list = []

            connections = self.get_connections(customer_id)

            oldest_connection = self.first_connection(customer_id, sensor)

            newest_connection = self.last_connection(customer_id, sensor)

            recent_playback = self.last_playback(customer_id)

            most_used_app = self.group_by_most_used_app(customer_id)

            most_used_device = self.group_by_most_used_device(customer_id)

            async for conn1 in connections:
                connection_startDate = datetime.strptime(
                    conn1["start"], "%Y-%m-%dT%H:%M:%S.%f"
                )
                connection_endDate = datetime.strptime(
                    conn1["end"], "%Y-%m-%dT%H:%M:%S.%f"
                )
                diff = connection_endDate - connection_startDate
                connection_time_list.append(diff / timedelta(milliseconds=1))

            async for app in most_used_app:
                playback_used_apps_list.append(
                    VisitedApps(app_name=app["_id"], visit_count=app["count"])
                )
                playback_most_used_app_list.append(app)

            async for device in most_used_device:
                most_used_device_list.append(device)

            async for date in oldest_connection:
                first_connection = date["data"]["startDate"]

            async for date2 in newest_connection:
                last_connection = date2["data"]["startDate"]

            async for playback in recent_playback:
                last_playback = playback

            # AVERAGE CONNECTION TIME
            last_playback_startDate = datetime.strptime(
                last_playback["data"]["playback_pair"]["startDate"],
                "%Y-%m-%dT%H:%M:%S.%f",
            )
            last_playback_endDate = datetime.strptime(
                last_playback["data"]["playback_pair"]["endDate"],
                "%Y-%m-%dT%H:%M:%S.%f",
            )

            playback_elapsed_time = int(
                (last_playback_endDate - last_playback_startDate)
                / timedelta(milliseconds=1)
            )

            if "metadata" in last_playback["data"]["playback_pair"]:
                playback_title = last_playback["data"]["playback_pair"]["metadata"][
                    "title"
                ]
            else:
                playback_title = "Not Specified"

            response = {
                "cast_response": {"status_code": status.HTTP_200_OK, "message": "Ok"},
                "cast_connections": len(connection_time_list),
                "cast_avg_connection_time": int(statistics.mean(connection_time_list)),
                "cast_visited_apps": playback_used_apps_list,
                "cast_most_visited_app": {
                    "app_name": playback_most_used_app_list[0]["_id"],
                    "app_visits": playback_most_used_app_list[0]["count"],
                    "app_avg_visit_time": int(
                        playback_most_used_app_list[0]["average"]
                    ),
                },
                "cast_first_connection": first_connection,
                "cast_last_connection": last_connection,
                "cast_most_used_device": {"device_id": most_used_device_list[0]["_id"]},
                "cast_last_playback": {
                    "playback_title": playback_title,
                    "playback_duration": playback_elapsed_time,
                    "playback_date": last_playback["data"]["playback_pair"][
                        "startDate"
                    ],
                },
            }
            return response
        except Exception as err:
            response = {
                "cast_meta_response": {
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": f"Customer doesn't have interaction with this sensor or has corrupted data: {err}",
                }
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)

    async def get_cast_history(
        self,
        customer_id: str,
        sensor: str,
        skip: Optional[int] = 0,
        limit: Optional[int] = None,
    ):
        playback_history_list = []
        playback_avg_time_list = []

        playback_count = await self.count__documents(customer_id, sensor)

        if playback_count > 0:

            playback_history = self.playback_history(customer_id, skip, limit)

            async for playback_item in playback_history:
                playback_startDate = datetime.strptime(
                    playback_item["data"]["playback_pair"]["startDate"],
                    "%Y-%m-%dT%H:%M:%S.%f",
                )
                playback_endDate = datetime.strptime(
                    playback_item["data"]["playback_pair"]["endDate"],
                    "%Y-%m-%dT%H:%M:%S.%f",
                )
                diff = playback_endDate - playback_startDate
                playback_avg_time_list.append(diff / timedelta(minutes=1))
                playback_history_list.append(
                    HistoryData(
                        date=playback_item["data"]["playback_pair"]["startDate"],
                        app=playback_item["data"]["playback_pair"]["appName"],
                        content=playback_item["data"]["playback_pair"]["content"],
                        duration=str(diff).split(".")[0],
                        device=playback_item["data"]["deviceId"],
                    )
                )
            response = {
                "playback_history_response": {
                    "status_code": status.HTTP_200_OK,
                    "message": "Ok",
                },
                "total_items": playback_count,
                "showing": limit,
                "skip": skip,
                "playback_history_data": playback_history_list,
            }
            return response
        else:
            response = {
                "playback_history_response": {
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Customer doesn't have interaction with this sensor",
                }
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
