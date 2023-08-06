from typing import Optional

from marshmallow_dataclass import dataclass

from tcgplayersdk.schemas.api_response import APIResponse
from tcgplayersdk.schemas.snake_case_schema import SnakeCaseSchema


@dataclass(base_schema=SnakeCaseSchema)
class Category():
    category_id: int
    seo_category_name: str
    modified_on: str
    display_name: str
    is_scannable: bool
    condition_guide_url: str
    sealed_label: Optional[str]
    non_sealed_label: Optional[str]
    name: str
    popularity: int
    is_direct: bool


@dataclass(base_schema=SnakeCaseSchema)
class CategoriesResponse(APIResponse):
    total_items: int
    results: list[Category]
