from typing import Any

from core.connection.connection import ConnectionMongo


class SegmenterDetailsRepo(ConnectionMongo):
    def __init__(self):
        super().__init__()

    async def create_segment(self, data: dict[str, str]) -> Any:
        new_segment: Any = await self.segments.insert_one(data)

        return new_segment
