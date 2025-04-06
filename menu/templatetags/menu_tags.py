from django import template

register = template.Library()

# 매장 매핑 데이터 (새로운 매장은 여기만 추가)
STORE_MAP = {
    "A": "서초점",
    "B": "강남점",
    # "C": "홍대점",  # 예시로 주석 처리된 매장
}

# 카테고리 매핑 데이터 (새로운 카테고리는 여기만 추가)
CATEGORY_MAP = {
    "bread": "빵",
    "dessert": "디저트",
    # "cake": "케이크",  # 예시로 주석 처리된 카테고리
}

# 필터: 개별 매장 코드를 한국어로 변환
@register.filter
def store_to_korean(value):
    return STORE_MAP.get(value, value)

# 필터: 개별 카테고리 코드를 한국어로 변환
@register.filter
def category_to_korean(value):
    return CATEGORY_MAP.get(value, value)

# 커스텀 태그: 전체 매장 목록 반환
@register.simple_tag
def get_store_map():
    return STORE_MAP

# 커스텀 태그: 전체 카테고리 목록 반환
@register.simple_tag
def get_category_map():
    return CATEGORY_MAP