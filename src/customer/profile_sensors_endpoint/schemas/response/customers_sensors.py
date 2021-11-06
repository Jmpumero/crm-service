from typing import List, Optional, Any
from enum import Enum

from pydantic import BaseModel


class PmsHistoryListConstrains(Enum):
    booking_code = "Booking"
    booking_date = "Fecha"
    booking_min_amt = "Monto min."
    booking_max_amt = "Monto max."


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
    app_avg_visit_time: Optional[int]


class MostUsedDevice(BaseModel):
    device_vendor: Optional[str]
    device_count: Optional[int]


class LastPlayback(BaseModel):
    playback_title: Optional[str]
    playback_duration: Optional[int]
    playback_date: Optional[str]


class HistoryData(BaseModel):
    date: Optional[str]
    app: Optional[str]
    content: Optional[str]
    duration: Optional[str]
    device: Optional[str]


class PlaybackHistory(BaseModel):
    playback_history_response: Response
    total_items: int
    showing: int
    skip: Optional[int]
    playback_history_data: Optional[List[HistoryData]]


class VisitedApps(BaseModel):
    app_name: str
    visit_count: int


class CastResponse(BaseModel):
    cast_response: Response
    cast_connections: Optional[int]
    cast_avg_connection_time: Optional[int]
    cast_visited_apps: Optional[List[VisitedApps]]
    cast_most_visited_app: Optional[MostVisitedApp]
    cast_first_connection: Optional[str]
    cast_last_connection: Optional[str]
    cast_most_used_device: Optional[MostUsedDevice]
    cast_last_playback: Optional[LastPlayback]


class HotspotResponse(BaseModel):
    hotspot_response: Response
    hotspot_connections: Optional[int]
    hotspot_used_devices: Optional[List[MostUsedDevice]]
    hotspot_first_connection: Optional[str]
    hotspot_last_connection: Optional[str]


class PmsStay(BaseModel):
    date: Optional[str]
    property: Optional[str]
    duration: Optional[int]
    room_type: Optional[str]
    upgrade: Optional[int]
    upselling: Optional[int]
    amount: Optional[float]


class PmsBook(BaseModel):
    code: Optional[str]
    checkin: Optional[str]
    checkout: Optional[str]
    cost: Optional[float]
    room_type: Optional[str]
    rate_plan: Optional[str]
    currency: Optional[str]
    reseller: Optional[str]
    meal_plan: Optional[str]
    property: Optional[str]
    taxes: Optional[str]


class PmsResponse(BaseModel):
    pms_response: Response
    pms_first_stay: Optional[PmsStay]
    pms_last_stay: Optional[PmsStay]
    pms_avg_stay: Optional[int]
    pms_most_used_room_type: Optional[str]
    pms_total_income: Optional[float]
    pms_avg_pax: Optional[float]
    pms_last_used_room_type: Optional[str]
    pms_consolidate_nights: Optional[int]
    pms_avg_anticipation: Optional[float]
    pms_cancelled_bookings: Optional[int]
    pms_preferred_sales_channel: Optional[str]
    pms_total_lodge_income: Optional[float]


class PmsHistorySecondaryGuest(BaseModel):
    book_code: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    documentId: Optional[List[DocumentID]]
    age: Optional[int]


class PmsHistoryPrimaryGuest(BaseModel):
    book_code: Optional[str]
    name: Optional[str]
    last_name: Optional[str]
    nationality: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    email: Optional[str]
    documentId: Optional[List[DocumentID]]
    civil_status: Optional[str]
    age: Optional[int]
    languages: Optional[str]
    country: Optional[str] = None
    city: Optional[str]
    booking: Optional[PmsBook]
    companion_data: Optional[List[PmsHistorySecondaryGuest]]


class PmsHistory(BaseModel):
    pms_history_response: Response
    total_items: int
    showing: int
    skip: int
    guest_data: Optional[List[PmsHistoryPrimaryGuest]]
    companion_data: Optional[List[PmsHistorySecondaryGuest]]
    booking_data: Optional[List[PmsBook]]


class SensorsTab(BaseModel):
    response: Response
    sensors_list: List[str]
