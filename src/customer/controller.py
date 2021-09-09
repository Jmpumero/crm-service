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


@customers_router.get("/customers/{customer_id}/profile-header")
@remove_422
async def get_customer_profile_header(customer_id: int):
    service = Service()

    return service.get_profile_header(customer_id)


@customers_router.get("/customers/{customer_id}/details")
@remove_422
async def get_customer_profile_detail(customer_id: int):
    service = Service()

    return service.get_profile_details(customer_id)
