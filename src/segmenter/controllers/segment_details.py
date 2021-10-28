from fastapi import APIRouter, Depends

from core import keycloack_guard
from ..services import SegmentDetailsService
from ..schemas import CreateSegment
from utils.remove_422 import remove_422


segments_details_router: APIRouter = APIRouter(
    tags=["Segment Detail"], dependencies=[Depends(keycloack_guard)]
)


@segments_details_router.get("/segments/{segments_id}/details")
async def get_segmenter_details(segmenter_id: str) -> str:

    return "it's works"


@segments_details_router.post("/segments")
@remove_422
async def create_segment(body: CreateSegment) -> dict[str, str]:
    service: SegmentDetailsService = SegmentDetailsService()

    return await service.create_segment(body)
