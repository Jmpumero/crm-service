from fastapi import APIRouter, Depends

from core import keycloack_guard
from ..services import CreativityService
from ..schemas import CreateCreativity

creativity_router: APIRouter = APIRouter(
    tags=["Creativity"], dependencies=[Depends(keycloack_guard)]
)


@creativity_router.get("/creativity/")
async def get_all_creativities():
    service = CreativityService()

    return await service.get_all()


@creativity_router.post("/creativity/")
async def get_all_creativities(body: CreateCreativity):
    service = CreativityService()

    return await service.create_creativity(body)
