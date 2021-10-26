from typing import List, Optional, Any

from pydantic import BaseModel


class Response(BaseModel):
    status_code: int
    message: str

class DocumentID(BaseModel):
    documentType: str
    documentNumber: str


class Phones(BaseModel):
    local_format: Optional[str]
    intl_format: str
    areaCode: Optional[str]
    countryCode: Optional[str]
    isMain: bool


class Emails(BaseModel):
    email: str
    isMain: bool


class Languages(BaseModel):
    language: str
    isMain: bool

class Addresses(BaseModel):
    address: str
    isMain: bool

class MostVisitedApp(BaseModel):
    app_name: Optional[str]
    app_visits: Optional[int]
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
    playback_history_response: Response
    id: str
    total_items: int
    showing: int
    skip: Optional[int]
    playback_history_data:Optional[List[HistoryData]]

class VisitedApps(BaseModel):
    app_name: str
    visit_count: int

class CastResponse(BaseModel):
    cast_response: Response
    id: str
    cast_connections: Optional[int]
    cast_avg_connection_time: Optional[str]
    cast_visited_apps: Optional[List[VisitedApps]]
    cast_most_visited_app: Optional[MostVisitedApp]
    cast_first_connection: Optional[str]
    cast_last_connection: Optional[str]
    cast_most_used_device: Optional[MostUsedDevice]
    cast_last_playback: Optional[LastPlayback]

class HotspotResponse(BaseModel):
    hotspot_response: Response
    id: str
    hotspot_connections: Optional[int]
    #hotspot_used_devices: Optional[List[MostUsedDevice]]
    hotspot_first_connection: Optional[str]
    hotspot_last_connection: Optional[str]

class PmsStay(BaseModel):
    date: Optional[str]
    property: Optional[str]
    duration: Optional[str]
    room_type: Optional[str]
    upgrade: Optional[int]
    upselling: Optional[int]
    amount: Optional[float] 

class PmsBooking(BaseModel):
    pms_book_code: Optional[str]
    pms_book_checkin: Optional[str]
    pms_book_checkout: Optional[str]
    pms_book_cost: Optional[float]
    pms_book_room_type: Optional[str]
    pms_book_rate_plat: Optional[str]
    pms_book_currency: Optional[str]
    pms_book_reseller: Optional[str]
    pms_book_meal_plan: Optional[str]
    pms_book_property: Optional[str]
    pms_book_taxes: Optional[str]

class PmsResponse(BaseModel):
    pms_response: Response
    pms_first_stay: Optional[PmsStay]
    pms_last_stay: Optional[PmsStay]
    pms_avg_stay: Optional[str]
    pms_most_used_room_type: Optional[str]
    pms_total_income: Optional[float]
    pms_avg_pax: Optional[float]
    pms_last_used_room_type: Optional[str]
    pms_consolidate_nights: Optional[int]
    pms_avg_anticipation: Optional[float]
    pms_cancelled_bookings: Optional[int]
    pms_preferred_sales_channel: Optional[str]
    pms_total_lodge_income: Optional[float]


class PmsHistory(BaseModel):
    pms_history_response: Response
    pms_history_name: Optional[str]
    pms_history_last_name: Optional[str]
    pms_history_nationality: Optional[List[str]]
    pms_history_phone: Optional[List[Phones]]
    pms_history_address: Optional[List[Addresses]]
    pms_history_email: Optional[List[Emails]]
    pms_history_documentId: Optional[List[DocumentID]]
    pms_history_civil_status: Optional[str]
    pms_history_age: Optional[int]
    pms_history_languages: Optional[List[Languages]]
    pms_history_country: Optional[str] = None
    pms_history_city: Optional[str]
    pms_booking: Optional[PmsBooking]

