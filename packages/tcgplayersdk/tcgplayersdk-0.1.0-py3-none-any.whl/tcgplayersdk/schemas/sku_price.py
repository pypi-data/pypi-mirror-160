from typing import Optional

from marshmallow_dataclass import dataclass

from tcgplayersdk.schemas.api_response import APIResponse
from tcgplayersdk.schemas.snake_case_schema import SnakeCaseSchema


@dataclass(base_schema=SnakeCaseSchema)
class SkuPrice():
    sku_id: int
    lowest_shipping: Optional[float]
    lowest_listing_price: Optional[float]
    low_price: float
    market_price: float
    direct_low_price: Optional[float]


@dataclass
class SkuPricesResponse(APIResponse):
    results: list[SkuPrice]
