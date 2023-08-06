import sys

from tcgplayersdk.schemas.product import Product


def sort_by_number(cards: list[Product], key='Number'):
    def get_sort_value(card: Product, key=key):
        r = card.get_number(key=key)
        return sys.maxsize if r is None else card.group_id * 400 + int(r)

    return sorted(cards, key=get_sort_value)
