from fastapi import APIRouter, status, Depends

from typing import Optional, Any

from core import keycloack_guard

from error_handlers.schemas.bad_gateway import BadGatewayError
from error_handlers.schemas.unauthorized import UnauthorizedError
from error_handlers.schemas.validation_error import CustomValidationError
from utils.remove_422 import remove_422

from ..services.cast_service import ProfileSensorsService
from ..schemas.response.customers_sensors import CastResponse

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

@sensor_router.get("/customers/search/profile/{customer_id}", 
    response_model=CastResponse,
    response_model_exclude_unset=True,
    responses={400: {"model": CustomValidationError}},
    status_code=201,
)
@remove_422
async def get_cast(customer_id: str, sensor: str):
    """
    Get sensor data from DW :
    """
    
    cast_stats = ProfileSensorsService()

    
    return await cast_stats.get_cast_stats(customer_id, sensor)

