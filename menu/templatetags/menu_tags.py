# 이후 매장 혹은 카테고리 추가될때 사용할 수 있도록 store_to_korean, category_to_korean 필터 추가
from django import template

register = template.Library()

@register.filter
def store_to_korean(value):
    store_map = {
        "A": "서초점",
        "B": "강남점",
        # "C": "홍대점",
    }
    return store_map.get(value, value)

@register.filter
def category_to_korean(value):
    category_map = {
        "bread": "빵",
        "dessert": "디저트",
        # "cake": "케이크",
    }
    return category_map.get(value, value)