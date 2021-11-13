import uuid

from ..schemas import CreateCreativity


creativities = {
    "skip": 0,
    "limit": 10,
    "column_sort": None,
    "order_sort": None,
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
        pass

    async def get_all(self):

        return creativities

    async def create_creativity(self, body):
        data = body.dict(by_alias=True)
        data["_id"] = str(uuid.uuid4())
        creativities["data"].append(data)

        return {"message": "creativity created successfully"}
