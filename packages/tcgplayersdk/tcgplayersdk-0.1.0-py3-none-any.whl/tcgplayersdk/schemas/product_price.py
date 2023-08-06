from typing import Optional

from marshmallow_dataclass import dataclass

from tcgplayersdk.schemas.api_response import APIResponse
from tcgplayersdk.schemas.snake_case_schema import SnakeCaseSchema


@dataclass(base_schema=SnakeCaseSchema)
class ProductPrice():
    product_id: int
    low_price: Optional[float]
    mid_price: Optional[float]
    high_price: Optional[float]
    market_price: Optional[float]
    direct_low_price: Optional[float]
    sub_type_name: Optional[str]


@dataclass
class ProductPricesResponse(APIResponse):
    results: list[ProductPrice]
