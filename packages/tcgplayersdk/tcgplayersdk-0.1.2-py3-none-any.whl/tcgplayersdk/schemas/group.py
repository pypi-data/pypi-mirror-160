from marshmallow_dataclass import dataclass

from tcgplayersdk.schemas.api_response import APIResponse
from tcgplayersdk.schemas.snake_case_schema import SnakeCaseSchema


@dataclass(base_schema=SnakeCaseSchema)
class Group():
    group_id: int
    name: str
    is_supplemental: bool
    published_on: str
    modified_on: str
    category_id: int
    abbreviation: str = None


@dataclass(base_schema=SnakeCaseSchema)
class GroupsResponse(APIResponse):
    total_items: int
    results: list[Group]
