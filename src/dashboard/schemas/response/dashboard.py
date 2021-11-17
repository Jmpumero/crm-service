from typing import List, Optional, Any
from enum import Enum

from pydantic import BaseModel, Field


class PmsGeneral(BaseModel):
    first_checkin: Optional[Any]
    first_checkout: Optional[Any]
    last_checkin: Optional[Any]
    last_checkout: Optional[Any]
    first_property: Optional[str]
    last_property: Optional[str]
    first_room_type: Optional[str]
    last_room_type: Optional[str]
    first_amount: Optional[int]
    last_amount: Optional[int]
    first_duration: Optional[int]
    last_duration: Optional[int]


class Forecasts(BaseModel):
    concept: Optional[str]
    count: Optional[int]
    net_amount: Optional[float]
    avg_income: Optional[float]


class Upsellings(BaseModel):
    total_upsellings: Optional[int]
    total_upsellings_income: Optional[float]


class FoodBeverages(BaseModel):
    total_paid: Optional[float]
    consuptions_amount: Optional[int]
    avg_consuption_expenses: Optional[float]


### ACTIVITY


class RevenueDistribution(BaseModel):
    pass


class RevenuePerStay(BaseModel):
    pass


class CancellationPercentage(BaseModel):
    cancelled: float = Field(...)
    non_cancelled: float = Field(...)


class TopTenSoldUpsellings(BaseModel):
    pass


class RedeemedPromosPercentage(BaseModel):
    pass


class UpsellingsOverRevenue(BaseModel):
    total_revenue: float = Field(...)
    upselling_revenue: float = Field(...)


class TopSellingProducts(BaseModel):
    pass


class CustomersAgeRange(BaseModel):

    param_1: str
    param_2: str


class CustomersGenderRatio(BaseModel):
    pass


# DIRECT CHANNEL


class DirectReservationPercentage(BaseModel):
    pass


class ExpenseTypePerCustomer(BaseModel):
    pass


class UpsellingOverTotalPercentage(BaseModel):
    pass


class TopTenSoldUpsellingsDirect(BaseModel):
    pass


class DashBoardActivity(BaseModel):
    revenue_distribution: Optional[RevenueDistribution]
    revenue_per_stay: Optional[RevenuePerStay]
    cancellation_perc: Optional[CancellationPercentage]
    top_ten_upsellings: Optional[TopTenSoldUpsellings]
    redeemed_promos: Optional[RedeemedPromosPercentage]
    extras_over_revenue: Optional[UpsellingsOverRevenue]
    top_selling_products: Optional[TopSellingProducts]
    customer_age_range: Optional[CustomersAgeRange]
    customer_gender_ratio: Optional[CustomersGenderRatio]
    direct_reservations_perc: Optional[DirectReservationPercentage]
    direct_reservation_expense_type: Optional[ExpenseTypePerCustomer]
    direct_reservation_up_over_total_exp_perc: Optional[UpsellingOverTotalPercentage]
    direct_reservation_topt_ten_sold_up: Optional[TopTenSoldUpsellingsDirect]


##DEMOGRAPHICS


class LodgingFunnel(BaseModel):
    pass


class LodgingFunnelPlusExtras(BaseModel):
    pass


class TypologyCustomerVolume(BaseModel):
    pass


class CustomerMoments(BaseModel):
    pass


class DashBoardDemographics(BaseModel):
    funnel: Optional[LodgingFunnel]
    funnel_plus_extras: Optional[LodgingFunnelPlusExtras]
    extras_over_revenue: Optional[UpsellingsOverRevenue]
    customer_gender_ratio: Optional[CustomersGenderRatio]
    typology_customer_volume: Optional[TypologyCustomerVolume]
    customer_moments: Optional[CustomerMoments]
    top_selling_products: Optional[TopSellingProducts]
    customer_age_range: Optional[CustomersAgeRange]
