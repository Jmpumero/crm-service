from typing import Optional

from fastapi import Query, Path
from fastapi import APIRouter, status, Depends

from core import keycloack_guard

from error_handlers.schemas.bad_gateway import BadGatewayError
from error_handlers.schemas.unauthorized import UnauthorizedError
from error_handlers.schemas.validation_error import CustomValidationError
from utils.remove_422 import remove_422

from ..services.cast_service import CastService
from ..services.hotspot_service import HotspotService
from ..services.pms_service import PmsService

from ..schemas.response.customers_sensors import CastResponse, HotspotResponse, PlaybackHistory
from ..schemas.response.customers_sensors import PmsResponse, PmsHistory

from config.config import Settings

global_settings = Settings()

sensor_router = APIRouter(
    tags=["Customer Profile - Sensors"],
    dependencies=[Depends(keycloack_guard)],
    responses={
        status.HTTP_502_BAD_GATEWAY: {"model": BadGatewayError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
    },
)


#CAST ENDPOINT
@sensor_router.get("/customer/{customer_id}/cast", 
    response_model=CastResponse,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": CustomValidationError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def get_cast(customer_id: str = Path(...)):
    """
    Get Customer Cast Usage Statistics\n
    **Input**:\n
    - **customer_id**: ID of customer in DW\n
    **Successful Response**:
    - **cast_response**: Server Response Code (200, 401, 404, 502)
    - **cast_customer_id**: ID of customer in DW
    - **cast_connections**: Number of Customer Connections to Cast
    - **cast_avg_connection_time**: Average Time of Customer Connection to Cast
    - **cast_visited_apps**: All Visited Applications Data (Name, Visits)
    - **cast_most_visited_app**: Most Visited Application Data (Name, Visits, Average Visit Time)
    - **cast_first_connection**: Date of First Connection to Cast
    - **cast_last_connection**: Date of Last Connection to Cast
    - **cast_most_used_device**: Most Used Device ID in DW
    - **cast_last_playback**: Last Cast Playback Data (Title, Duration, Playback Date)
    """

    cast_stats = CastService()
    return await cast_stats.get_cast_stats(customer_id, 'sensor_2')

#CAST HISTORY ENDPOINT
@sensor_router.get("/customer/{customer_id}/cast-history", 
    response_model=PlaybackHistory,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": CustomValidationError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def get_cast_history(customer_id: str = Path(...), 
                           skip: Optional[int] = 0, 
                           limit: int = Query(default=global_settings.pagination_limit)):
    """
    Get Cast Playback History from DW, given a Customer ID:\n
    **Input**:\n
    - **customer_id**: Customer ID in DW
    - **skip** : Paging number
    - **limit**: Max number of items to retrieve\n
    **Successful Response**:
    - **customer_id**: Customer ID in DW
    - **total_items**: Total Playbacks for the given Customer
    - **showing**: Number of Playbacks Displayed in this Search (**limit**)
    - **skip**: Paging Number
    - **playback_data**: List of Playbacks for te given **customer_id**
        - **date**: Playback Date
        - **app**: Used App,
        - **content**: Played Content
        - **duration**: Playback Duration
        - **device**: Used Device

    """

    hotspot_stats = CastService()
    return await hotspot_stats.get_cast_history(customer_id, 'sensor_2', skip, limit)

#HOTSPOT ENDPOINT
@sensor_router.get("/customer/{customer_id}/hotspot", 
    response_model=HotspotResponse,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": CustomValidationError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def get_hotspot(customer_id: str = Path(...)):
    """
    Get Customer Hotspot Usage Statistics:\n
    **Input**:\n
    - **customer_id**: ID of customer in DW\n
    **Successful Response**:
    - **hotspot_response**: Server Response Code (200, 401, 404, 502)
    - **hotspot_customer_id**: ID of customer in DW
    - **hotspot_connections**: Number of Customer Connections to Hotspot
    - **hotspot_first_connection**: Date of First Connection to Hotspot
    - **hotspot_last_connection**: Date of Last Connection to Hotspot
    """

    hotspot_stats = HotspotService()
    return await hotspot_stats.get_hotspot_stats(customer_id, sensor='sensor_3')


#PMS ENDPOINT
@sensor_router.get("/customer/{customer_id}/pms", 
    response_model=PmsResponse,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": CustomValidationError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def get_pms(customer_id: str = Path(...)):

    """
    Get Customer PMS Statistics:\n
    **Input**:\n
    
    **Successful Response**:
    
    """

    pms_stats = PmsService()
    return await pms_stats.get_pms_stats(customer_id, sensor='sensor_1')


#PMS BOOKING HISTORY ENDPOINT
@sensor_router.get("/customer/{customer_id}/pms-booking-history", 
    response_model=PmsHistory,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": CustomValidationError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def get_pms_history(customer_id: str, 
                          skip: Optional[int] = 0, 
                          limit: int = Query(default=global_settings.pagination_limit)):
    """
    Get PMS Booking History from DW, given a Customer ID:\n
    **Input**:\n
    
    **Successful Response**:
    
    """

    pms_history = PmsService()
    return await pms_history.get_pms_history(customer_id, 'sensor_1', skip, limit)