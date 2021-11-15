from typing import Any
from bson import ObjectId
from datetime import datetime

from ..repositories import SegmenterDetailsRepo, DemographyRepo
from ..schemas import CreateSegment, FilterSegment


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
        # print(updated_segment)
        return updated_segment

    async def update_status_segment(self, segment_id: str, status: str):
        updated_segment = await self.segmenter_detail_repo.find_and_update_status(
            segment_id, status
        )
        response = {"code": 401, "msg": "Segment not found"}

        if updated_segment != None:
            response = {"code": 200, "msg": "Segment update successfully"}
        return response

    async def get_one_segment(self, segment_id):

        r = await self.segmenter_detail_repo.find_one_segment(segment_id)
        # print(r)
        return r

    async def apply_filter_segment(self, data):

        result = await self.segmenter_detail_repo.apply_filter_segment(data.dict())

        return result
