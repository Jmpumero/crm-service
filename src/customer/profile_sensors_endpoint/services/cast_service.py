from datetime import datetime
from typing import Optional, Any
from ..schemas.response.customers_sensors import PlaybackHistory
from src.customer.profile_sensors_endpoint.repository.cast.cast_queries import CastQueries

class CastService(CastQueries):
    def __init__(self):
        super().__init__()

    async def get_cast_stats(self, customer_id: str, sensor : str) -> Any:

        playback_history_list = []

        count = await self.connection_number(customer_id, sensor)
        
        oldest_connection = self.first_connection(customer_id, sensor)
        
        newest_connection = self.last_connection(customer_id, sensor)

        oldest_playback = self.last_playback(customer_id)

        playback_history = self.playback_history(customer_id, sensor)



        async for date in oldest_connection:
            first_connection = date['data']['startDate']

        async for date2 in newest_connection:
            last_connection = date2['data']['startDate']

        async for playback in oldest_playback:
            last_playback = playback

        async for playback_item  in playback_history:
            playback_startDate = datetime.strptime(playback_item['data']['playback_pair']['startDate'], '%Y-%m-%dT%H:%M:%S.%f')
            playback_endDate = datetime.strptime(playback_item['data']['playback_pair']['endDate'], '%Y-%m-%dT%H:%M:%S.%f')

            playback_history_list.append(PlaybackHistory(playback_history_date = playback_item['data']['playback_pair']['startDate'],
                                                        playback_history_app= playback_item['data']['playback_pair']['appName'],
                                                        playback_history_content= playback_item['data']['playback_pair']['content'],
                                                        playback_history_duration= str(playback_endDate - playback_startDate),
                                                        playback_history_device= playback_item['data']['deviceId']))

        
        #AVERAGE CONNECTION TIME
        
        
        last_playback_startDate = datetime.strptime(last_playback['data']['playback_pair']['startDate'], '%Y-%m-%dT%H:%M:%S.%f')
        last_playback_endDate = datetime.strptime(last_playback['data']['playback_pair']['endDate'], '%Y-%m-%dT%H:%M:%S.%f')

        playback_elapsed_time = last_playback_endDate - last_playback_startDate



        response = {
            'cast_connections': count,
            'cast_first_connection': first_connection,
            'cast_last_connection': last_connection,
            "cast_last_playback": {
                "playback_title": last_playback['data']['playback_pair']['metadata']['title'],
                "playback_duration": str(playback_elapsed_time),
                "playback_date": last_playback['data']['playback_pair']['startDate']
            },
            "cast_playback_history":  playback_history_list

        }
        
        return response
