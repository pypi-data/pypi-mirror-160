import logging
from typing import Optional, Type

import requests
from schemas.category import CategoriesResponse
from schemas.group import Group, GroupsResponse
from schemas.identity import Identity
from schemas.product import ProductsResponse
from schemas.product_price import ProductPricesResponse
from schemas.sku_price import SkuPricesResponse

from tcgplayersdk.decorators import require_category
from tcgplayersdk.exceptions import TCGPlayerSDKException
from tcgplayersdk.schemas.api_response import APIResponse
from tcgplayersdk.schemas.product import SkuItem

TCGPLAYER_BASE_URL = 'https://api.tcgplayer.com'
TCGPLAYER_API_VERSION = 'v1.39.0'
TCGPLAYER_API_URL = f'{TCGPLAYER_BASE_URL}/{TCGPLAYER_API_VERSION}'

log = logging.getLogger(__name__)


class TCGPlayerSDK():
    def __init__(
        self,
        public_key: str,
        private_key: str,
        categoryId: Optional[int] = None,
        log_requests: Optional[int] = None,
    ):
        self.public_key = public_key
        self.private_key = private_key
        self.categoryId = categoryId
        self.log_requests = log_requests

        self._requests_patched = False
        self._identity: Optional[Identity] = None
        self._session = requests.Session()

    @property
    def session(self):
        if self._identity is None or self._identity.is_expired():
            r = requests.post(
                f'{TCGPLAYER_API_URL}/token',
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.public_key,
                    'client_secret': self.private_key,
                },
            )
            self._identity = Identity.from_json(r.json())
            self._session.headers.update({
                'Authorization': f'{self._identity.token_type} {self._identity.access_token}',
            })

        if self.log_requests is not None and not self._requests_patched:
            old_request_method = self._session.request
            def log_and_request(method, url,
                    params=None, data=None, headers=None, cookies=None, files=None,
                    auth=None, timeout=None, allow_redirects=True, proxies=None,
                    hooks=None, stream=None, verify=None, cert=None, json=None
                ):
                # I hate this logger so much
                msg = '%s %s'
                args = [method.upper(), url]
                if params is not None:
                    msg += ' params=%s'
                    args.append(params)
                if data is not None:
                    msg += ' data=%s'
                    args.append(data)
                if json is not None:
                    msg += ' json=%s'
                    args.append(json)
                log.log(self.log_requests, msg, *args)

                return old_request_method(method, url,
                    params, data, headers, cookies, files,
                    auth, timeout, allow_redirects, proxies,
                    hooks, stream, verify, cert, json,
                )
            self._session.request = log_and_request
        self._requests_patched = True
        return self._session

    def _get_all_pages(self, path: str, cls: Type[APIResponse], extra_params={}):
        res: APIResponse = None
        offset = 0
        limit = 100

        while True:
            r = self.session.get(
                path,
                params={
                    **extra_params,
                    'offset': offset,
                    'limit': 100,
                }
            )
            if r.status_code != 200:
                raise TCGPlayerSDKException(r)

            parsed: APIResponse = cls.Schema().loads(r.text)

            if res is None:
                res = parsed
            else:
                res.results.extend(parsed.results)

            offset += limit
            if len(res.results) >= res.total_items:
                break

        return res

    def get_categories(self, sort_order='name', sort_desc=False) -> CategoriesResponse:
        return self._get_all_pages(
            f'{TCGPLAYER_API_URL}/catalog/categories',
            CategoriesResponse,
            extra_params={
                'sortOrder': sort_order,
                'sortDesc': sort_desc,
            }
        )

    @require_category
    def get_all_groups(self, categoryId=None) -> GroupsResponse:
        return self._get_all_pages(
            f'{TCGPLAYER_API_URL}/catalog/categories/{categoryId}/groups',
            GroupsResponse,
        )

    def get_products_in_group(
        self,
        group_or_groupId: Group|int|str,
        product_types='cards',
        get_extended_fields=False,
        include_skus=False
    ) -> ProductsResponse:
        group_id = group_or_groupId.group_id if isinstance(group_or_groupId, Group) else group_or_groupId

        return self._get_all_pages(
            f'{TCGPLAYER_API_URL}/catalog/products',
            ProductsResponse,
            extra_params={
                'groupId': group_id,
                'productTypes': product_types,
                'getExtendedFields': str(get_extended_fields).lower(),
                'includeSkus': str(include_skus).lower(),
            }
        )

    def get_product_prices_in_group(self, group_or_groupId: Group|int|str,) -> ProductPricesResponse:
        group_id = group_or_groupId.group_id if isinstance(group_or_groupId, Group) else group_or_groupId
        r = self.session.get(
            f'{TCGPLAYER_API_URL}/pricing/group/{group_id}',
        )
        return ProductPricesResponse.Schema().load(r.json())

    def get_prices_for_skus(self, skus: list[SkuItem|int|str],) -> SkuPricesResponse:
        sku_list = ','.join([str(sku.sku_id if isinstance(skus, SkuItem) else sku) for sku in skus])

        # TODO: Verify that this doesn't break a URL length limit
        r = self.session.get(
            f'{TCGPLAYER_API_URL}/pricing/sku/{sku_list}',
        )
        return SkuPricesResponse.Schema().load(r.json())


if __name__ == '__main__':
    import os

    from tcgplayersdk.category_enum import Categories
    # from tcgplayersdk.sdk import TCGPlayerSDK
    from tcgplayersdk.util import sort_by_number

    tcgplayer = TCGPlayerSDK(
        os.getenv('PKMN_DECKLIST_TCGPLAYER_PUBLIC_KEY'),
        os.getenv('PKMN_DECKLIST_TCGPLAYER_PRIVATE_KEY'),
        categoryId=Categories.POKEMON,
        log_requests=logging.WARNING,
    )

    base_set = tcgplayer.get_products_in_group(604, get_extended_fields=True, include_skus=True)
    fossil = tcgplayer.get_products_in_group(630, get_extended_fields=True, include_skus=True)
    jungle = tcgplayer.get_products_in_group(635, get_extended_fields=True, include_skus=True)

    all_products = sort_by_number(base_set.results + fossil.results + jungle.results)

    skus = [card.get_sku([2], [10, 11, 122, 123]) for card in all_products]
    sku_prices = tcgplayer.get_prices_for_skus(skus)

    for card, sku in zip(all_products, sku_prices.results):
        print(f'{card.get_number()},{card.name},{sku.sku_id},{sku.lowest_listing_price},{card.url}')
