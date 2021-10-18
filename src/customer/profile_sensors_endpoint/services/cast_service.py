from datetime import datetime
from typing import Optional, Any
from src.customer.profile_sensors_endpoint.repository.cast.cast_queries import CastQueries

class ProfileSensorsService(CastQueries):
    def __init__(self):
        super().__init__()

    async def get_cast_stats(self, customer_id: str, sensor : str) -> Any:

        count = await self.connection_number(customer_id, sensor)
        
        oldest_connection = self.first_connection(customer_id, sensor)
        
        newest_connection = self.last_connection(customer_id, sensor)

        oldest_playback = self.last_playback(customer_id)

        async for date in oldest_connection:
            first_connection = date['data']['startDate']

        async for date2 in newest_connection:
            last_connection = date2['data']['startDate']

        async for playback in oldest_playback:
            last_playback = playback


        playback_startDate = datetime.strptime(last_playback['data']['playback_pair']['startDate'], '%Y-%m-%dT%H:%M:%S.%f')
        playback_endDate = datetime.strptime(last_playback['data']['playback_pair']['endDate'], '%Y-%m-%dT%H:%M:%S.%f')

        playback_elapsed_time = playback_endDate - playback_startDate

        response = {
            'cast_connections': count,
            'cast_first_connection': first_connection,
            'cast_last_connection': last_connection,
            "cast_last_playback": {
                "playback_title": last_playback['data']['playback_pair']['metadata']['title'],
                "playback_duration": str(playback_elapsed_time),
                "playback_date": last_playback['data']['playback_pair']['startDate']
            },

        }
        
        return response
