from typing import List, Optional, Any
from pydantic import BaseModel


class Response(BaseModel):
    status_code: int
    message: str

class MostVisitedApp(BaseModel):
    app_name: Optional[str]
    app_avg_visit_time: Optional[str]
    app_usual_visit_hour: Optional[str]

class MostVisitedAppGraph(BaseModel):
    app_name: Optional[int]
    app_avg_visit_time: Optional[str]

class MostUsedDevice(BaseModel):
    device_id : Optional[str]
    
class LastPlayback(BaseModel):
    playback_title: Optional[str]
    playback_duration: Optional[str]
    playback_date: Optional[str]

class HistoryData(BaseModel):
    date: Optional[str]
    app: Optional[str]
    content: Optional[str]
    duration: Optional[str]
    device: Optional[str]

class PlaybackHistory(BaseModel):
    playback_history_meta_response: Response
    playback_history_count: int
    playback_history_data:Optional[List[HistoryData]]

class CastResponse(BaseModel):
    cast_meta_response: Response
    cast_connections: Optional[int]
    cast_avg_connection_time: Optional[str]
    cast_most_visited_app: Optional[MostVisitedApp]
    cast_most_visited_app_graph: Optional[List[MostVisitedAppGraph]]
    cast_first_connection: Optional[str]
    cast_last_connection: Optional[str]
    cast_most_used_device: Optional[MostUsedDevice]
    cast_last_playback: Optional[LastPlayback]

class HotspotResponse(BaseModel):
    hotspot_meta_response: Response
    hotspot_connections: Optional[int]
    hotspot_used_devices: Optional[List[MostUsedDevice]]
    hotspot_avg_connection_time: Optional[str]
    hotspot_first_connection: Optional[str]
    hotspot_last_connection: Optional[str]


