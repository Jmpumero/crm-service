from os import sync
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

    async def find_one_segment(self, id):

        return await self.segments.find_one({"_id": id})

    async def find_one_and_update(
        self, segment_id: str, updated_segment: UpdatedSegment
    ) -> Any:
        body_update = updated_segment.dict()

        segment: Any = await self.segments.find_one_and_update(
            {"_id": segment_id},
            {"$set": body_update},
            return_document=ReturnDocument.AFTER,
        )

        return segment

    async def find_and_update_status(self, segment_id, status):

        return await self.segments.find_one_and_update(
            {"_id": segment_id},
            {"$set": {"status": status}},
        )
