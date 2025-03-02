from django.shortcuts import render
from django.db.models import Sum
from django.db.models.functions import TruncDate
from kiosk.models import OrderItem, OrderInfo, Item

from datetime import datetime, timedelta

# 오늘 날짜 가져오기
today = datetime.today().date()
five_days_ago = today - timedelta(days=5)  # 어제부터 5일간의 범위로 변경

def sales_main(request):
    store = request.user.member.store  # 사용자의 매장 정보 가져오기

    # GET 요청에서 기간과 제품 ID 가져오기 (없으면 기본값: 최근 5일)
    start_date = request.GET.get("start_date", five_days_ago.strftime("%Y-%m-%d"))
    end_date = request.GET.get("end_date", today.strftime("%Y-%m-%d"))
    item_id = request.GET.get("item_id", "all")  # 'all'이면 전체 제품

    # 날짜 형식 변환
    start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
    end_date = datetime.strptime(end_date, "%Y-%m-%d").date()

    # 📌 주문 데이터 필터링
    query = OrderItem.objects.filter(order__store=store, order__order_at__date__range=[start_date, end_date])

    # 특정 제품만 조회하는 경우
    if item_id != "all":
        query = query.filter(item_id=item_id)

    # 날짜별 제품 판매량 집계
    sales_data = (
        query.annotate(order_date=TruncDate('order__order_at'))  # 날짜만 추출
        .values('order_date', 'item_id')  # 날짜별 & 제품별 그룹화
        .annotate(total_quantity=Sum('item_count'))  # 제품별 총 수량 계산
        .order_by('order_date')  # 날짜순 정렬
    )

    # 제품 정보 매핑 (item_id -> 제품명, 판매가)
    item_map = {item.item_id: {"name": item.item_name, "price": item.sale_price} for item in Item.objects.all()}

    # 최종 데이터 변환
    formatted_sales_data = []
    for sale in sales_data:
        item_id = sale["item_id"]
        item_info = item_map.get(item_id, {"name": "알 수 없음", "price": 0})
        total_price = sale["total_quantity"] * item_info["price"]

        formatted_sales_data.append({
            "date": sale["order_date"],
            "item_id": item_id,
            "item_name": item_info["name"],
            "total_quantity": f"{sale['total_quantity']:,}",  # 쉼표 추가
            "total_price": f"{total_price:,}"  # 쉼표 추가
        })

    # 전체 판매 내역에서 상위 5개 판매 제품 가져오기 (총 수량 기준)
    total_sales_data = (
        OrderItem.objects.filter(order__store=store)  # 모든 판매 데이터를 가져옴
        .values('item_id')  # 제품별로 그룹화
        .annotate(total_quantity=Sum('item_count'))  # 총 수량 계산
        .order_by('-total_quantity')  # 총 수량 내림차순 정렬
    )

    top5_products = []
    for sale in total_sales_data[:5]:  # 상위 5개 제품
        item_id = sale["item_id"]
        item_info = item_map.get(item_id, {"name": "알 수 없음", "price": 0})
        total_price = sale["total_quantity"] * item_info["price"]

        top5_products.append({
            "item_id": item_id,
            "item_name": item_info["name"],
            "total_quantity": f"{sale['total_quantity']:,}",  # 쉼표 추가
            "total_price": f"{total_price:,}"  # 쉼표 추가
        })

    # 제품 목록 가져오기 (필터 선택용)
    items = Item.objects.values("item_id", "item_name")

    context = {
        "sales_data": formatted_sales_data,
        "top5": top5_products,  # 전체 판매 내역을 기준으로 상위 5개 제품
        "items": items,
        "member": request.user.member,
        "selected_item": item_id,
        "selected_start_date": start_date,
        "selected_end_date": end_date
    }

    return render(request, "sales/sales_main.html", context)
