from typing import Optional

from marshmallow_dataclass import dataclass

from tcgplayersdk.schemas.api_response import APIResponse
from tcgplayersdk.schemas.snake_case_schema import SnakeCaseSchema


@dataclass
class PresaleInfo():
    isPresale: bool
    releasedOn: str = None
    note: str = None


@dataclass
class ExtendedInfoItem():
    name: str
    displayName: str
    value: str


@dataclass(base_schema=SnakeCaseSchema)
class SkuItem():
    sku_id: int
    product_id: int
    condition_id: int
    printing_id: int
    language_id: int


@dataclass(base_schema=SnakeCaseSchema)
class Product():
    product_id: int
    name: str
    clean_name: str
    image_url: str
    category_id: int
    group_id: int
    url: str
    modified_on: str
    image_count: Optional[int]                      # getExtendedInfo=True
    presale_info: Optional[PresaleInfo]             # getExtendedInfo=True
    extended_data: Optional[list[ExtendedInfoItem]] # getExtendedInfo=True
    skus: Optional[list[SkuItem]]                   # includeSkus=True

    def get_number(self, key='Number') -> str|None:
        if self.extended_data is None:
            return None

        for info in self.extended_data:
            if info.name == key:
                return info.value

        return None

    def get_sku(self, condition_ids, printing_ids, language_id=1) -> int|None:
        if self.extended_data is None:
            return None

        for sku in self.skus:
            if sku.language_id == language_id and sku.printing_id in printing_ids and sku.condition_id in condition_ids:
                return int(sku.sku_id)

        return None


@dataclass(base_schema=SnakeCaseSchema)
class ProductsResponse(APIResponse):
    total_items: Optional[int]
    results: list[Product]
