from typing import Any, Optional

from fastapi import status
from fastapi.responses import JSONResponse

from src.customer.profile_sensors_endpoint.repository.sensors_tab import (
    SensorsTabQueries,
)


class SensorsTabService(SensorsTabQueries):
    """
    Service to get PMS usage statistics

    """

    def __init__(self):
        super().__init__()

    async def get_sensors_tab(self, customer_id):
        try:
            sensors = await self.get_associated_sensors(customer_id)

            response = {
                "response": {"status_code": status.HTTP_200_OK, "message": "Ok"},
                "sensors_list": sensors["associated_sensors"],
            }

            return response
        except:
            response = {
                "response": {
                    "status_code": status.HTTP_404_NOT_FOUND,
                    "message": "Customer doesn't have interaction with this sensor",
                }
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)
