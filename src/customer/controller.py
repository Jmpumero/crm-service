from fastapi import APIRouter, Depends

from .service import Service

from .schemas import SearchCustomersQueryParams

from utils.remove_422 import remove_422

customers_router = APIRouter(
    tags=["Customers"],
)


@customers_router.get("/customers/")
@remove_422
async def get_customers(
    query_params: SearchCustomersQueryParams = Depends(SearchCustomersQueryParams),
):
    service = Service()

    return service.get(query_params)
