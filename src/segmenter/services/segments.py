from typing import Any
from bson import ObjectId

from ..repositories import SegmenterDetailsRepo, DemographyRepo
from ..schemas import CreateSegment


class SegmentDetailsService:
    def __init__(self):
        self.segmenter_detail_repo = SegmenterDetailsRepo()
        self.test = DemographyRepo()

    async def create_segment(self, segment: CreateSegment):
        new_segment: Any = await self.segmenter_detail_repo.create_segment(
            {"_id": str(ObjectId()), "name": segment.segment_name}
        )

        return {
            "segment_id": new_segment.inserted_id,
            "name": segment.segment_name,
        }

    async def update_segment(self, segment_id: str, segment: Any):
        updated_segment = await self.segmenter_detail_repo.find_one_and_update(
            segment_id, segment
        )

        return updated_segment

    async def test_segments(self, data):

        date = {"from_": 3654256987, "to": 1578962454123}
        t = ""
        t = await self.test.test_beta_query(data)

        return t
