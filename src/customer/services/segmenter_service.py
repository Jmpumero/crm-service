from typing import Any

from src.customer.repository import MongoQueries
from src.customer.repositories import SegmenterQueries
from src.customer.schemas.get.query_params import SegmenterQueryParams
from src.customer.schemas.get.responses.segmenter import SegmenterResponse


class SegmenterService(MongoQueries):
    def __init__(self):
        super().__init__()
        self.repository = SegmenterQueries()

    async def get_author_segments_list(self) -> Any:
        authors = {}
        try:
            authors = await self.repository.get_all_author_in_segments()
            authors = await authors.to_list(length=None)

            list_authors = []

            for x in range(len(authors)):
                list_authors.append(authors[x]["author"])

        except Exception as e:
            print(e)
        return list_authors

    async def get_segmenters(
        self, query_params: SegmenterQueryParams
    ) -> SegmenterResponse:

        segments = {}

        try:
            result = await self.repository.find_segments(query_params)
            result = await result.to_list(length=query_params.limit)
            author = await self.get_author_segments_list()
            if result != None and author != None:
                segments["total_items"] = result[0]["total_items"][0]["total_items"]
                segments["total_shows"] = result[0]["total_show"][0]["show_items"]
                segments["items"] = result[0]["segments"]
                segments["authors"] = author
                segments["global_total_clients"] = await self.total_customer()
                segments["total_enable_clients"] = (
                    await self.total_customer()
                ) - await self.total_customer_in_blacklist(True)

        except Exception as e:
            print(e)
            segments["total_items"] = 0
            segments["total_shows"] = 0
            segments["items"] = []
            segments["authors"] = []
            segments["global_total_clients"] = 0
            segments["total_enable_clients"] = 0
            result = None

        return SegmenterResponse(**segments)
