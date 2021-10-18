from typing import List, Optional, Any
from pydantic import BaseModel


class MostUsedApp(BaseModel):
    app_name: Optional[int]
    app_avg_visit_time: Optional[str]
    app_usual_visit_hour: Optional[str]

class MostUsedDevice(BaseModel):
    device_id : Optional[str]
    
class LastPlayback(BaseModel):
    playback_title: Optional[str]
    playback_duration: Optional[str]
    playback_date: Optional[str]

class PlaybackHistory(BaseModel):
    playback_history_date: Optional[str]
    playback_history_app: Optional[str]
    playback_history_date: Optional[str]
    playback_history_content: Optional[str]
    playback_history_duration: Optional[str]
    playback_history_device: Optional[str]

class CastResponse(BaseModel):
    cast_connections: Optional[int]
    cast_avg_connection_time: Optional[str]
    cast_most_used_app: Optional[MostUsedApp]
    cast_first_connection: Optional[str]
    cast_last_connection: Optional[str]
    cast_most_used_device: Optional[MostUsedDevice]
    cast_last_playback: Optional[LastPlayback]
    cast_playback_history: Optional[List[PlaybackHistory]]

