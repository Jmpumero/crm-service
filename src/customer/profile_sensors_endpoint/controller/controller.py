from fastapi import APIRouter, status, Depends

from typing import Optional

from core import keycloack_guard

from error_handlers.schemas.bad_gateway import BadGatewayError
from error_handlers.schemas.unauthorized import UnauthorizedError
from error_handlers.schemas.validation_error import CustomValidationError
from utils.remove_422 import remove_422

from ..services.cast_service import CastService
from ..services.hotspot_service import HotspotService
from ..schemas.response.customers_sensors import CastResponse, HotspotResponse, PlaybackHistory

from config.config import Settings

global_settings = Settings()

sensor_router = APIRouter(
    tags=["Sensors"],
    dependencies=[Depends(keycloack_guard)],
    responses={
        status.HTTP_502_BAD_GATEWAY: {"model": BadGatewayError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
    },
)


#CAST ENDPOINT
@sensor_router.get("/customers/search/profile/cast/{customer_id}", 
    response_model=CastResponse,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": CustomValidationError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def get_cast(customer_id: str):
    """
    Get sensor data from DW :
    """

    cast_stats = CastService()
    return await cast_stats.get_cast_stats(customer_id, 'sensor_2')


#CAST HISTORY ENDPOINT
@sensor_router.get("/customers/search/profile/cast/history/{customer_id}", 
    response_model=PlaybackHistory,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": CustomValidationError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def get_cast_history(customer_id: str, skip: Optional[int] = None, limit: Optional[int] = None):
    """
    Get sensor data from DW :
    """

    hotspot_stats = CastService()
    return await hotspot_stats.get_cast_history(customer_id, skip, limit)

#HOTSPOT ENDPOINT
@sensor_router.get("/customers/search/profile/hotspot/{customer_id}", 
    response_model=HotspotResponse,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": CustomValidationError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def get_hotspot(customer_id: str, sensor: str):
    """
    Get sensor data from DW :
    """

    hotspot_stats = HotspotService()
    return await hotspot_stats.get_hotspot_stats(customer_id, sensor)

