from src.customer.repository import MongoQueries
from typing import Any, Coroutine


class SegmenterQueries(MongoQueries):
    def __init__(self):
        super().__init__()

    def column_sort(self, column):

        column_target = "name"

        if column.lower() == "author":
            column_target = "author"
        elif column.lower() == "ultima actualizacion":
            column_target = "updated_at"
        elif column.lower() == "estado":
            column_target = "status"
        elif column.lower() == "fecha de creacion":
            column_target = "created_at"
        elif column.lower() == "clientes":
            column_target = "clients"
        return column_target

    def filter_match(self, params) -> dict:
        match_build = {}
        match_build["$match"] = {}

        if params.status != None:
            match_build["$match"]["status"] = params.status
        if params.tag != None:
            tags = params.tag.replace("[", "").replace("]", "").split(",")
            match_build["$match"]["tags"] = {"$in": tags}
        if params.author != None:
            match_build["$match"]["author"] = params.author

        return dict(match_build)

    def search_match(self, item) -> dict:

        match = {
            "$match": {
                "$or": [
                    {
                        "name": {
                            "$regex": f".*{item}.*",
                            "$options": "i",
                        }
                    },
                    {
                        "author": {
                            "$regex": f".*{item}.*",
                            "$options": "i",
                        }
                    },
                    {
                        "updated_at": {
                            "$regex": f".*{item}.*",
                            "$options": "i",
                        }
                    },
                    {
                        "status": {
                            "$regex": f".*{item}.*",
                            "$options": "i",
                        }
                    },
                    {
                        "created_at": {
                            "$regex": f".*{item}.*",
                            "$options": "i",
                        }
                    },
                ]
            }
        }

        return dict(match)

    async def find_segments(self, params) -> Coroutine:
        result = None
        order = 1

        column_target = self.column_sort(params.column_sort)
        if params.order_sort == "desc":
            order = -1

        match_filter = self.filter_match(params)
        if params.query != None:
            match_search = self.search_match(params.query)
        else:
            match_search = self.search_match("")

        result = self.segments.aggregate(
            [
                {
                    "$facet": {
                        "total_items": [
                            match_filter,
                            match_search,
                            {
                                "$project": {
                                    "_id": 1,
                                }
                            },
                            {"$count": "total_items"},
                        ],
                        "total_show": [
                            match_filter,
                            match_search,
                            {
                                "$project": {
                                    "_id": 1,
                                }
                            },
                            {"$skip": params.skip},
                            {"$limit": params.limit},
                            {"$count": "show_items"},
                        ],
                        "segments": [
                            match_filter,
                            match_search,
                            {
                                "$project": {
                                    "filter": 0,
                                    "applied_filters": 0,
                                }
                            },
                            {"$skip": params.skip},
                            {"$limit": params.limit},
                            {
                                "$sort": {
                                    f"{column_target}": order,
                                    "_id": 1,
                                }
                            },
                        ],
                    }
                },
            ]
        )

        return result

    async def get_all_author_in_segments(self) -> Coroutine:

        final_response = {}
        authors = self.segments.aggregate(
            [
                {
                    "$project": {
                        "author": 1,
                        "_id": 0,
                    }
                },
            ]
        )

        return authors
