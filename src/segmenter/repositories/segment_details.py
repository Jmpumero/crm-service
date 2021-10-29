from typing import Any

from pymongo import ReturnDocument

from ..schemas import UpdatedSegment
from core.connection.connection import ConnectionMongo


class SegmenterDetailsRepo(ConnectionMongo):
    def __init__(self):
        super().__init__()

    async def create_segment(self, data: dict[str, str]) -> Any:
        new_segment: Any = await self.segments.insert_one(data)

        return new_segment

    async def find_one_and_update(
        self, segment_id: str, updated_segment: UpdatedSegment
    ) -> Any:
        segment: Any = await self.segments.find_one_and_update(
            {"_id": segment_id},
            {"$set": updated_segment.dict()},
            return_document=ReturnDocument.AFTER,
        )

        return segment
