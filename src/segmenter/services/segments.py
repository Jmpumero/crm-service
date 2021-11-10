from typing import Any
from bson import ObjectId
from datetime import datetime

from ..repositories import SegmenterDetailsRepo, DemographyRepo
from ..schemas import CreateSegment


class SegmentService:
    def __init__(self):
        self.segmenter_detail_repo = SegmenterDetailsRepo()
        self.test = DemographyRepo()

    async def create_segment(self, segment: CreateSegment):

        today = datetime.utcnow()
        today = datetime.strftime(today, "%Y-%m-%dT%H:%M:%S.%f")
        new_segment: Any = await self.segmenter_detail_repo.create_segment(
            {
                "_id": str(ObjectId()),
                "name": segment.segment_name,
                "create_at": today,
                "update_at": today,
                "author": segment.author.lower(),
                "status": "draft",
            }
        )

        return {
            "segment_id": new_segment.inserted_id,
        }

    async def update_segment(self, segment_id: str, segment: Any):
        updated_segment = await self.segmenter_detail_repo.find_one_and_update(
            segment_id, segment
        )

        return updated_segment

    async def update_status_segment(self, segment_id: str, status: str):
        updated_segment = await self.segmenter_detail_repo.find_and_update_status(
            segment_id, status
        )

        return updated_segment

    async def get_one_segment(self, segment_id):

        return await self.segmenter_detail_repo.find_one_segment(segment_id)

    async def test_segments(self, data):

        date = {"from_": 3654256987, "to": 1578962454123}
        t = ""
        t = await self.test.test_beta_query(data)

        return t
