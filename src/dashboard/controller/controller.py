from typing import Optional

from fastapi import Query, Path
from fastapi import APIRouter, status, Depends

from core import keycloack_guard

from http_exceptions import BadGatewayError, UnauthorizedError, NotFoundError

from utils.remove_422 import remove_422

from src.dashboard.schemas.response.dashboard import (
    DashBoardActivity,
    DashBoardDemographics,
)

from ..services import DashBoardService

from config.config import Settings

global_settings = Settings()

dashboard_router = APIRouter(
    tags=["Dashboard"],
    dependencies=[Depends(keycloack_guard)],
    responses={
        status.HTTP_502_BAD_GATEWAY: {"model": BadGatewayError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnauthorizedError},
    },
)

# Activity endpoint
@dashboard_router.get(
    "/dashboard/activity",
    summary="Dashboard Activity Tab",
    response_model=DashBoardActivity,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def dashboard_activity(
    date_from: str = Query(default=None),
    date_to: str = Query(default=None),
    property: str = Query(default=None),
    segment: str = Query(default=None),
):
    """
    Activity Dashboard
    """

    service = DashBoardService()
    return await service.get_activity_graphs(date_from, date_to, property, segment)


# Demographics endpoint
@dashboard_router.get(
    "/dashboard/demographics",
    summary="Dashboard Demographics Tab",
    response_model=DashBoardDemographics,
    response_model_exclude_unset=True,
    responses={status.HTTP_404_NOT_FOUND: {"model": NotFoundError}},
    status_code=status.HTTP_200_OK,
)
@remove_422
async def dashboard_demographics(
    date_from: str = Query(default=None),
    date_to: str = Query(default=None),
    property: str = Query(default=None),
    segment: str = Query(default=None),
):
    """
    Demographics Dashboard
    """

    service = DashBoardService()
    return await service.get_demographics_graphs(date_from, date_to, property, segment)
