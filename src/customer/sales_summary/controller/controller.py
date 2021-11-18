from typing import Optional

from fastapi import Query, Path
from fastapi import APIRouter, status, Depends

from core import keycloack_guard

from http_exceptions import BadGatewayError, UnauthorizedError, NotFoundError

from utils.remove_422 import remove_422

from ..schemas.response.sales_summary_response import SalesSummaryResponse
from ..services.sales_summary_service import SalesSummaryService

from config.config import Settings

global_settings = Settings()

sales_summary_router = APIRouter(
    tags=["Customer Profile - Sales Summary"],
    dependencies=[Depends(keycloack_guard)],
    responses={
        status.HTTP_502_BAD_GATEWAY: {"model": BadGatewayError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
    },
)

# Sales Summary Tab ENDPOINT
@sales_summary_router.get(
    "/customer/{customer_id}/sales_summary",
    summary="Sales Summary Tab in Customer Profile",
    response_model=SalesSummaryResponse,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def get_get_sales_summary(customer_id: str = Path(...)):
    """
    Get Customer Sensors list
    """

    sensors = SalesSummaryService()
    return await sensors.get_sales_summary_graphs(customer_id)
