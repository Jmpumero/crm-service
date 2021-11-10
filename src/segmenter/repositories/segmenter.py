from os import sync
from typing import Any

from pymongo import ReturnDocument
from datetime import datetime

from ..schemas import UpdatedSegment, FilterSegment
from core.connection.connection import ConnectionMongo

from .demography_querys import DemographyRepo


class SegmenterDetailsRepo(ConnectionMongo):
    def __init__(self):
        super().__init__()
        self.demography = DemographyRepo()

    async def create_segment(self, data: dict[str, str]) -> Any:
        new_segment: Any = await self.segments.insert_one(data)

        return new_segment

    async def find_one_segment(self, id):

        return await self.segments.find_one({"_id": id})

    async def find_one_and_update(
        self, segment_id: str, updated_segment: UpdatedSegment
    ) -> Any:
        body_update = self.demography.convert_date_update(updated_segment.dict())
        # print(body_update)

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

    async def apply_filter_segment(self, data: dict) -> Any:

        array_filters = data["applied_filters"]
        date_range = data["date_range"]
        print(date_range)
        for filter in array_filters:
            if filter["filter_name"] == "demography":
                print(filter)
