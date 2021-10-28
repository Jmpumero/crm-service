from typing import Any
from bson import ObjectId

from pymongo.errors import DuplicateKeyError

from ..repositories import SegmenterDetailsRepo
from ..schemas import CreateSegment


class SegmentDetailsService:
    def __init__(self):
        self.segmenter_detail_repo = SegmenterDetailsRepo()

    async def create_segment(self, segment: CreateSegment):
        new_segment: Any = await self.segmenter_detail_repo.create_segment(
            {"_id": str(ObjectId()), "name": segment.segment_name}
        )

        return {
            "segmenter_id": new_segment.inserted_id,
            "name": segment.segment_name,
        }
