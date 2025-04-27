from django.shortcuts import render
from kiosk.models import OrderItem, OrderInfo, Item
from collections import defaultdict
from django.db.models import Sum

def sales_main(request):
    # ✅ 현재 로그인한 사용자의 매장 정보
    store = request.user.member.store

    # ✅ GET 요청으로부터 필터 조건(시작일, 종료일, 선택 상품) 수신
    startDate = request.GET.get("startDate")
    endDate = request.GET.get("endDate")
    selectedProduct = request.GET.get("selectedProduct")

    # ✅ 전체 상품이 선택되었는지에 따라 상품 리스트 필터링
    if selectedProduct == "전체":
        product_list = Item.objects.all().order_by("item_name")
    else:
        product_list = Item.objects.filter(store=store).order_by("item_name")

    # ✅ 주문 항목 데이터를 집계 (주문ID, 상품ID 기준으로 묶어서 총 판매액, 수량 합계 계산)
    result = (
        OrderItem.objects.filter(order__store=store)
        .values("order_id", "item_id")
        .annotate(
            item_total_amount=Sum("item_total"),
            item_total_count=Sum("item_count"),
        )
    )

    # ✅ item_id → 상품명, 판매가, 원가 매핑용 딕셔너리 생성
    item_map = {
        item.item_id: {"name": item.item_name, "price": item.sale_price, "cost_price" : item.cost_price }
        for item in Item.objects.all()
    }

    # ✅ order_id → 주문일 매핑용 딕셔너리 생성
    order_map = {
        order.order_id: {"name": order.order_at}
        for order in OrderInfo.objects.all()
    }

    # ✅ 날짜별 상품 판매 내역 저장 리스트
    date_item_amounts = []

    for sale in result:
        order_id = sale["order_id"]
        order_data = order_map.get(order_id)
        order_date = order_data.get("name") if order_data else None

        if order_date:
            order_date = order_date.strftime("%Y-%m-%d")  # 날짜 문자열 변환

            # ⛔ 선택한 기간 외의 데이터는 제외
            if startDate and endDate:
                if not (startDate <= order_date <= endDate):
                    continue

        item_id = sale["item_id"]
        item_info = item_map.get(item_id, {"name": "알 수 없음", "price": 0, "cost_price": 0})
        # cost_price = item_info.get("cost_price", 0)
        item_total_cost = item_info["cost_price"] * sale["item_total_count"] # 원가 * 수량


        # ⛔ 특정 제품만 필터링
        if selectedProduct and selectedProduct != "전체":
            if item_info["name"] != selectedProduct:
                continue


        date_item_amounts.append(
            {
                "order_date": order_date,
                "item_id": item_id,
                "item_name": item_info["name"],
                "item_total_count": sale["item_total_count"],
                "item_total_amount": sale["item_total_amount"],
                "item_total_cost": item_total_cost,
            }
        )

    # ✅ (날짜, 제품)별 데이터 통합
    grouped_sales = defaultdict(
        lambda: {"order_date": None, "item_id": None, "item_name": None, "item_total_count": 0, "item_total_amount": 0, "item_total_cost": 0, "item_profit": 0}
    )

    for sale in date_item_amounts:
        key = (sale["order_date"], sale["item_id"])
        grouped_sales[key]["order_date"] = sale["order_date"]
        grouped_sales[key]["item_id"] = sale["item_id"]
        grouped_sales[key]["item_name"] = sale["item_name"]
        grouped_sales[key]["item_total_count"] += sale["item_total_count"]
        grouped_sales[key]["item_total_amount"] += sale["item_total_amount"]
        grouped_sales[key]["item_total_cost"] += sale["item_total_cost"]
        grouped_sales[key]["item_profit"] = (
                grouped_sales[key]["item_total_amount"] - grouped_sales[key]["item_total_cost"]
        )

    # ✅ 날짜 + 제품별 정리된 매출 데이터
    final_sales = list(grouped_sales.values())

    # ✅ 날짜별 전체 매출액 계산
    date_total_sales = defaultdict(lambda: {"order_date": None, "total_sales": 0, "total_cost": 0, "profit": 0})

    for sale in final_sales:
        date = sale["order_date"]
        date_total_sales[date]["order_date"] = date
        date_total_sales[date]["total_sales"] += sale["item_total_amount"]
        date_total_sales[date]["total_cost"] += sale.get("item_total_cost", 0)
        date_total_sales[date]["profit"] = (
                date_total_sales[date]["total_sales"] - date_total_sales[date]["total_cost"]
        )

    date_total_sales = list(date_total_sales.values())

    # ✅ 제품별 총 판매량 계산
    final_total_counts = defaultdict(
        lambda: {"order_date": None, "item_id": None, "item_name": None, "item_total_count": 0, "item_total_amount": 0}
    )

    for sale in final_sales:
        item_id = sale["item_id"]
        final_total_counts[item_id]["order_date"] = sale["order_date"]
        final_total_counts[item_id]["item_id"] = item_id
        final_total_counts[item_id]["item_name"] = sale["item_name"]
        final_total_counts[item_id]["item_total_count"] += sale["item_total_count"]
        final_total_counts[item_id]["item_total_amount"] += sale["item_total_amount"]

    # ✅ Top 5 판매량 기준 제품 추출
    final_total_counts_list = list(final_total_counts.values())
    final_total_counts_list.sort(key=lambda x: x["item_total_count"], reverse=True)
    top_5_sales = final_total_counts_list[:5]

    # ✅ Top 5 제품에 해당하는 데이터만 필터링
    top_5_item_ids = {item["item_id"] for item in top_5_sales}
    top_5_filtered_sales = [sale for sale in final_sales if sale["item_id"] in top_5_item_ids]

    # ✅ 최종 context 전달
    context = {
        "final_sales": final_sales,
        "date_total_sales": date_total_sales,
        "top_5_sales": top_5_sales,
        "top_5_filtered_sales": top_5_filtered_sales,
        "member": request.user.member,
        "product_list": product_list,
        "selectedProduct": selectedProduct,
        "startDate": startDate,
        "endDate": endDate,
    }

    return render(request, "sales/sales_main.html", context)
