from fastapi import APIRouter, Depends
from fastapi import Body
from fastapi.param_functions import Path

from core import keycloack_guard
from src.segmenter.schemas.get import response
from src.segmenter.schemas.put.update_segment import UpdateStatusSegment
from ..services import SegmentService
from ..schemas import (
    CreateSegment,
    UpdatedSegment,
    SegmentDetails,
    UpdateStatusSegment,
    GenericResponse,
    FilterSegment,
)
from http_exceptions import BadRequestError
from utils.remove_422 import remove_422

from src.segmenter import services


segments_details_router: APIRouter = APIRouter(
    tags=["Segmenter"], dependencies=[Depends(keycloack_guard)]
)


@segments_details_router.get(
    "/segments/{segment_id}/details",
    responses={400: {"model": BadRequestError}},
    response_model=SegmentDetails,
)
@remove_422
async def get_segmenter_details(segment_id: str = Path(...)) -> any:
    service = SegmentService()
    return await service.get_one_segment(segment_id)


@segments_details_router.post("/segments")
@remove_422
async def create_segment(body: CreateSegment) -> dict[str, str]:
    service: SegmentService = SegmentService()

    return await service.create_segment(body)


@segments_details_router.put(
    "/segments/{segment_id}",
    responses={400: {"model": BadRequestError}},
)
@remove_422
async def update_segment(
    segment_id: str = Path(...), body: UpdatedSegment = Body(...)
) -> dict[str, str]:
    service: SegmentService = SegmentService()

    return await service.update_segment(segment_id, body)


@segments_details_router.put(
    "/segments/{segment_id}",
    responses={400: {"model": BadRequestError}},
)
@remove_422
async def update_segment(
    segment_id: str = Path(...), body: UpdatedSegment = Body(...)
) -> dict[str, str]:
    service: SegmentService = SegmentService()

    return await service.update_segment(segment_id, body)


@segments_details_router.put(
    "/segments/{segment_id}/status",
    response_model=GenericResponse,
    responses={400: {"model": BadRequestError}},
)
@remove_422
async def update_status_segment(
    segment_id: str = Path(...), body: UpdateStatusSegment = Body(...)
) -> dict[str, str]:
    service: SegmentService = SegmentService()
    return await service.update_status_segment(segment_id, body.status)


@segments_details_router.post(
    "/segment/filters",
    responses={400: {"model": BadRequestError}},
)
@remove_422
async def update_segment(body: FilterSegment = Body(...)) -> dict[str, str]:
    service: SegmentService = SegmentService()

    return await service.apply_filter_segment(body)
