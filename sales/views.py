from django.shortcuts import render
from kiosk.models import OrderItem, OrderInfo, Item
from collections import defaultdict
from django.db.models import Sum

def sales_main(request):
    store = request.user.member.store  # 사용자의 매장 정보 가져오기

    # 사용자가 선택한 기간 가져오기 (YYYY-MM-DD 형식으로 가정)
    startDate = request.GET.get("startDate")
    endDate = request.GET.get("endDate")
    selectedProduct = request.GET.get("selectedProduct")

    # "전체"가 선택된 경우 모든 상품을 가져오고, 선택된 매장에 대한 경우는 필터링하여 가져옵니다.
    if selectedProduct == "전체":
        product_list = Item.objects.all().order_by("item_name")  # 모든 매장의 제품
    else:
        product_list = Item.objects.filter(store=store).order_by("item_name")  # 해당 매장 제품

    # 📌 주문 데이터 필터링
    result = (
        OrderItem.objects.filter(order__store=store)
        .values("order_id", "item_id")
        .annotate(
            item_total_amount=Sum("item_total"),  # 총 판매액 계산
            item_total_count=Sum("item_count"),  # 총 판매량 계산
        )
    )

    # 제품 정보 매핑 (item_id -> 제품명, 판매가)
    item_map = {item.item_id: {"name": item.item_name, "price": item.sale_price} for item in Item.objects.all()}

    # 주문 정보 매핑 (order_id -> 주문 날짜)
    order_map = {order.order_id: {"name": order.order_at} for order in OrderInfo.objects.all()}

    # 첫 단계 데이터 리스트 생성
    date_item_amounts = []
    for sale in result:
        order_id = sale["order_id"]
        order_data = order_map.get(order_id)
        order_date = order_data.get("name") if order_data else None

        if order_date:
            order_date = order_date.strftime("%Y-%m-%d")  # 날짜 형식 변환

            # 📌 기간 필터링 추가
            if startDate and endDate:
                if not (startDate <= order_date <= endDate):
                    continue  # 선택한 기간 밖이면 제외

        item_id = sale["item_id"]
        item_total_count = sale["item_total_count"]
        item_info = item_map.get(item_id, {"name": "알 수 없음", "price": 0})
        item_total_amount = sale["item_total_amount"]

        # 📌 제품 필터링 추가
        if selectedProduct and selectedProduct != "전체":
            if item_info["name"] != selectedProduct:
                continue  # 선택한 제품이 아니면 제외

        date_item_amounts.append(
            {
                "order_date": order_date,
                "item_id": item_id,
                "item_name": item_info["name"],
                "item_total_count": item_total_count,
                "item_total_amount": item_total_amount,
            }
        )

    # 📌 날짜 & 제품별 매출 데이터 그룹화
    grouped_sales = defaultdict(
        lambda: {"order_date": None, "item_id": None, "item_name": None, "item_total_count": 0, "item_total_amount": 0}
    )

    for sale in date_item_amounts:
        order_date = sale["order_date"]
        item_id = sale["item_id"]
        item_name = sale["item_name"]
        item_total_count = sale["item_total_count"]
        item_total_amount = sale["item_total_amount"]

        grouped_sales[(order_date, item_id)]["order_date"] = order_date
        grouped_sales[(order_date, item_id)]["item_id"] = item_id
        grouped_sales[(order_date, item_id)]["item_name"] = item_name
        grouped_sales[(order_date, item_id)]["item_total_count"] += item_total_count
        grouped_sales[(order_date, item_id)]["item_total_amount"] += item_total_amount

    # 🚀 `final_sales`는 특정 제품 & 특정 기간의 매출 데이터
    final_sales = list(grouped_sales.values())

    # 📌 날짜별 총 매출 계산 (전체 그래프)
    date_total_sales = defaultdict(lambda: {"order_date": None, "total_sales": 0})

    for sale in final_sales:
        order_date = sale["order_date"]
        item_total_amount = sale["item_total_amount"]

        date_total_sales[order_date]["order_date"] = order_date
        date_total_sales[order_date]["total_sales"] += item_total_amount
    # 🚀 `date_total_sales`는 선택한 기간의 전체 매출 데이터
    date_total_sales = list(date_total_sales.values())  # 결과를 리스트로 변환

    # 제품별 총 판매량 계산(전체 top5)
    final_total_counts = defaultdict(lambda: {"order_date": None, "item_id": None, "item_name": None, "item_total_count": 0, "item_total_amount": 0})

    for sale in final_sales:
        order_date = sale["order_date"]
        item_id = sale["item_id"]
        item_name = sale["item_name"]
        item_total_count = sale["item_total_count"]
        item_total_amount = sale["item_total_amount"]

        # 제품별 총 판매량을 합산
        final_total_counts[item_id]["order_date"] = order_date
        final_total_counts[item_id]["item_id"] = item_id
        final_total_counts[item_id]["item_name"] = item_name
        final_total_counts[item_id]["item_total_count"] += final_total_counts[item_id].get("item_total_count", 0) + item_total_count
        final_total_counts[item_id]["item_total_amount"] += final_total_counts[item_id].get("item_total_amount", 0) + item_total_amount

    # 결과를 리스트로 변환
    final_total_counts_list = list(final_total_counts.values())

    # item_total_count 기준으로 내림차순 정렬
    final_total_counts_list.sort(key=lambda x: x["item_total_count"], reverse=True)

    # 상위 5개만 선택 (Top 5)
    top_5_sales = final_total_counts_list[:5]

    # 📌 Top 5 제품만 필터링한 판매 데이터 생성
    top_5_item_ids = {item["item_id"] for item in top_5_sales}  # Top 5 제품 ID 집합
    top_5_filtered_sales = [sale for sale in final_sales if sale["item_id"] in top_5_item_ids]

    context = {
        "final_sales": final_sales,  # 날짜별 총 판매액 결과
        "date_total_sales": date_total_sales,  # 날짜별 총 판매액 결과
        "top_5_sales": top_5_sales,  # 제품별 총 판매량 결과
        "top_5_filtered_sales": top_5_filtered_sales,  # Top 5 제품의 판매 추이 데이터
        "member": request.user.member,  # 사용자 정보
        "product_list": product_list,
        "selectedProduct": selectedProduct,
        "startDate": startDate,
        "endDate": endDate,

    }

    return render(request, "sales/sales_main.html", context)
