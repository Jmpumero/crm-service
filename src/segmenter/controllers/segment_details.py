from fastapi import APIRouter, Depends

from core import keycloack_guard

segmenter_details_router: APIRouter = APIRouter(
    tags=["Customer Profile"], dependencies=[Depends(keycloack_guard)]
)


@segmenter_details_router.get("segmenter/{segmenter_id}/details")
async def get_segmenter_details(segmenter_id: str) -> str:

    return "hooola mundo"
