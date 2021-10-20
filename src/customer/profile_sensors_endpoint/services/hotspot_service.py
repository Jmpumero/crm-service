import statistics
from datetime import datetime, timedelta
from typing import Any

from starlette import status
from ..schemas.response.customers_sensors import PlaybackHistory
from src.customer.profile_sensors_endpoint.repository.cast_hotspot import CastHotSpotQueries

from fastapi.responses import JSONResponse

class HotspotService(CastHotSpotQueries):
    def __init__(self):
        super().__init__()

    async def get_hotspot_stats(self, customer_id: str, sensor : str) -> Any:
        try:
            count = await self.count__documents(customer_id, sensor)

            oldest_connection = self.first_connection(customer_id, sensor)
            
            newest_connection = self.last_connection(customer_id, sensor)

            async for date in oldest_connection:
                first_connection = date['data']['date']

            async for date2 in newest_connection:
                last_connection = date2['data']['date']

            response = {
                'hotspot_meta_response':{
                    'status_code':status.HTTP_200_OK,
                    'message': 'Ok'
                },
                'hotspot_connections': count,
                'hotspot_first_connection': first_connection,
                'hotspot_last_connection': last_connection
            }
            return response
        except:
            response = {
                'cast_meta_response':{
                    'status_code':status.HTTP_404_NOT_FOUND,
                    'message': "Customer doesn't have interaction with this sensor"
                }
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response)