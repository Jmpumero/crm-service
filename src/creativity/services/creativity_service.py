import uuid
from bson import ObjectId

from ..schemas import CreateCreativity, GetAllQueryParams
from ..repositories import CreativityRepo

creativities_response = {
    "skip": 0,
    "limit": 10,
    "column_sort": None,
    "order_sort": None,
    "total_items": 10,
    "query": "",
    "data": [
        {
            "_id": "123456",
            "type": "email",
            "name": "d",
            "description": "dfs",
            "author": "Adrew",
        }
    ],
}


class CreativityService:
    def __init__(self):
        self.creativity_repo = CreativityRepo()

    async def get_all(self, query_params: GetAllQueryParams):
        creativities = (
            await self.creativity_repo.creativity.find()
            .skip(query_params.skip)
            .limit(query_params.limit)
            .to_list(length=query_params.limit)
        )

        creativities_response[
            "total_items"
        ] = await self.creativity_repo.creativity.count_documents({})
        creativities_response["skip"] = query_params.skip
        creativities_response["limit"] = query_params.limit
        creativities_response["data"] = creativities

        return creativities_response

    async def create_creativity(self, body: CreateCreativity):
        data = body.dict(by_alias=True)
        data["_id"] = str(ObjectId())

        await self.creativity_repo.creativity.insert_one(data)

        return {"message": "creativity created successfully"}

    async def get_one(self, creativity_id: str):
        creativity = await self.creativity_repo.creativity.find_one(
            {"_id": creativity_id}
        )

        return creativity or {}
