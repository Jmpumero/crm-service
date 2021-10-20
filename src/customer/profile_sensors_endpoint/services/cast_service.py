import statistics
from datetime import datetime, timedelta
from typing import Any, Optional

from starlette import status
from ..schemas.response.customers_sensors import HistoryData
from src.customer.profile_sensors_endpoint.repository.cast_hotspot import CastHotSpotQueries

from fastapi.responses import JSONResponse

class CastService(CastHotSpotQueries):
    def __init__(self):
        super().__init__()

    async def get_cast_stats(self, customer_id: str, sensor : str) -> Any:
        try:
            connection_avg_time_list = []
            playback_avg_time_list = []
            playback_most_used_app_list = []
            most_used_device_list = []

            count = self.count_connections(customer_id)

            connections = self.get_connections(customer_id, sensor)
            
            oldest_connection = self.first_connection(customer_id, sensor)
            
            newest_connection = self.last_connection(customer_id, sensor)

            recent_playback = self.last_playback(customer_id)

            most_used_app = self.group_by_most_used_app(customer_id)

            most_used_device = self.group_by_most_used_device(customer_id)

            playback_history = self.playback_history(customer_id, skip=None, limit=None)

            async for app in most_used_app:
                playback_most_used_app_list.append(app)

            async for device in most_used_device:
                most_used_device_list.append(device)

            async for date in oldest_connection:
                first_connection = date['data']['startDate']

            async for date2 in newest_connection:
                last_connection = date2['data']['startDate']

            async for playback in recent_playback:
                last_playback = playback

            async for conn in connections:
                connection_startDate = datetime.strptime(conn['data']['startDate'], '%Y-%m-%dT%H:%M:%S.%f')
                connection_endDate = datetime.strptime(conn['data']['endDate'], '%Y-%m-%dT%H:%M:%S.%f')
                diff = connection_endDate - connection_startDate
                connection_avg_time_list.append(diff/ timedelta(hours = 1))

            async for playback in playback_history:
                playback_startDate = datetime.strptime(playback['data']['playback_pair']['startDate'], '%Y-%m-%dT%H:%M:%S.%f')
                playback_endDate = datetime.strptime(playback['data']['playback_pair']['endDate'], '%Y-%m-%dT%H:%M:%S.%f')
                diff = playback_endDate - playback_startDate
                playback_avg_time_list.append(diff/ timedelta(hours = 1))

            #AVERAGE CONNECTION TIME
            last_playback_startDate = datetime.strptime(last_playback['data']['playback_pair']['startDate'], '%Y-%m-%dT%H:%M:%S.%f')
            last_playback_endDate = datetime.strptime(last_playback['data']['playback_pair']['endDate'], '%Y-%m-%dT%H:%M:%S.%f')
            
            playback_elapsed_time = round((last_playback_endDate - last_playback_startDate) / timedelta(hours = 1), 2)            

            response = {
                'cast_meta_response':{
                    'status_code':status.HTTP_200_OK,
                    'message': 'Ok'
                },
                'cast_connections': 0, #POR IMPLEMENTAR
                'cast_avg_connection_time': f"{round(statistics.mean(connection_avg_time_list), 2)} hours",
                'cast_most_visited_app': {
                    'app_name':playback_most_used_app_list[0]['_id'],
                    'app_avg_visit_time': f"{round(statistics.mean(playback_avg_time_list), 3)} hours",
                    'app_usual_visit_hour': 'POR IMPLEMENTAR'
                },
                'cast_first_connection': first_connection,
                'cast_last_connection': last_connection,
                'cast_most_used_device': {
                    'device_id':most_used_device_list[0]['_id']
                },
                "cast_last_playback": {
                    "playback_title": last_playback['data']['playback_pair']['metadata']['title'],
                    "playback_duration": f"{playback_elapsed_time} hours",
                    "playback_date": last_playback['data']['playback_pair']['startDate']
                }
            }
            return response
        except Exception as e:
            response = {
                'cast_meta_response':{
                    'status_code':status.HTTP_404_NOT_FOUND,
                    'message': f"Customer doesn't have interaction with this sensor {e}"
                }
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response) 

    async def get_cast_history(self, customer_id: str, skip: Optional[int] = None, limit: Optional[int] = None):
        playback_history_list = []
        playback_avg_time_list = []

        playback_count = await self.count__documents(customer_id, sensor='sensor_2')

        if playback_count > 0:
               
            playback_history = self.playback_history(customer_id, skip, limit)

            async for playback_item  in playback_history:
                playback_startDate = datetime.strptime(playback_item['data']['playback_pair']['startDate'], '%Y-%m-%dT%H:%M:%S.%f')
                playback_endDate = datetime.strptime(playback_item['data']['playback_pair']['endDate'], '%Y-%m-%dT%H:%M:%S.%f')
                diff = playback_endDate - playback_startDate
                playback_avg_time_list.append(diff/ timedelta(minutes = 1))
                playback_history_list.append(HistoryData(date = playback_item['data']['playback_pair']['startDate'],
                                                            app= playback_item['data']['playback_pair']['appName'],
                                                            content= playback_item['data']['playback_pair']['content'],
                                                            duration= str(diff).split('.')[0],
                                                            device= playback_item['data']['deviceId']))
            response = {
                'playback_history_meta_response':{
                    'status_code':status.HTTP_200_OK,
                    'message': 'Ok',
                },
                'playback_history_count': playback_count,
                'playback_history_data': playback_history_list
            }
            return response
        else:
            response = {
                'cast_meta_response':{
                    'status_code':status.HTTP_404_NOT_FOUND,
                    'message': "Customer doesn't have interaction with this sensor"
                }
            }
            return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content=response) 
        
        
