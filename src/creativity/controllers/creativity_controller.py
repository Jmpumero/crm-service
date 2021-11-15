from fastapi import APIRouter, Depends

from core import keycloack_guard
from ..services import CreativityService
from ..schemas import CreateCreativity, GetAllQueryParams
from utils.remove_422 import remove_422


creativity_router: APIRouter = APIRouter(
    tags=["Creativity"], dependencies=[Depends(keycloack_guard)]
)


@creativity_router.get("/creativity/")
@remove_422
async def get_all_creativities(
    query_params: GetAllQueryParams = Depends(GetAllQueryParams),
):
    service = CreativityService()

    return await service.get_all(query_params)


@creativity_router.post("/creativity/")
@remove_422
async def get_all_creativities(body: CreateCreativity):
    service = CreativityService()

    return await service.create_creativity(body)


@creativity_router.get("/creativity/{creativity_id}")
@remove_422
async def get_all_creativities(creativity_id: str):
    service = CreativityService()

    return await service.get_one(creativity_id)
