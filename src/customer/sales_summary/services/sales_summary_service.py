from typing import Any, Optional

from fastapi import status
from fastapi.responses import JSONResponse

from src.customer.sales_summary.repository.sales_summary_queries import (
    SalesSummaryQueries,
)


class SalesSummaryService(SalesSummaryQueries):
    """
    Service to get PMS usage statistics

    """

    def __init__(self):
        super().__init__()

    async def get_sales_summary_graphs(self, customer_id):
        response = {
            "total_revenue": None,
            "frequent_rooms": None,
            "most_contracted_services": None,
            "average_checkins": None,
            "most_visited_apps": None,
            "app_suite_usage": None,
            "app_frequency": None,
            "segment": None,
        }

        return response
