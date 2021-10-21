from typing import List, Optional, Any
from pydantic import BaseModel


class Response(BaseModel):
    status_code: int
    message: str

class MostVisitedApp(BaseModel):
    app_name: Optional[str]
    app_visits: Optional[int]
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
    response: Response
    _id: str
    total_items: int
    showing: int
    skip: Optional[int]
    data:Optional[List[HistoryData]]

class VisitedApps(BaseModel):
    app_name: str
    visit_count: int
    visit_average_time: Optional[int]

class CastResponse(BaseModel):
    cast_meta_response: Response
    cast_connections: Optional[int]
    cast_avg_connection_time: Optional[str]
    cast_visited_apps: Optional[List[VisitedApps]]
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


