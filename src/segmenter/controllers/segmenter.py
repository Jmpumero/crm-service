from fastapi import APIRouter, Depends
from fastapi import Body, Query

from core import keycloack_guard
from ..services import SegmentDetailsService
from ..schemas import CreateSegment, UpdatedSegment
from http_exceptions import BadRequestError
from utils.remove_422 import remove_422


segments_details_router: APIRouter = APIRouter(
    tags=["Segmenter"], dependencies=[Depends(keycloack_guard)]
)


@segments_details_router.get("/segments/{segment_id}/details")
async def get_segmenter_details(segment_id: str) -> str:

    return "it's works"


@segments_details_router.post("/segments")
@remove_422
async def create_segment(body: CreateSegment) -> dict[str, str]:
    service: SegmentDetailsService = SegmentDetailsService()

    return await service.create_segment(body)


@segments_details_router.put(
    "/segments/{segment_id}",
    responses={400: {"model": BadRequestError}},
)
@remove_422
async def update_segment(segment_id: str, body: UpdatedSegment) -> dict[str, str]:
    service: SegmentDetailsService = SegmentDetailsService()

    return await service.update_segment(segment_id, body)


@segments_details_router.get(
    "/segments/test/query",
    responses={400: {"model": BadRequestError}},
)
@remove_422
async def test_query_segment(body=Body(...)):
    service: SegmentDetailsService = SegmentDetailsService()
    # print(body)
    return await service.test_segments(body)
