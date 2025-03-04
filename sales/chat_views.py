from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from kiosk.models import OrderInfo, OrderItem
from datetime import timedelta
from django.utils.timezone import now
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

FASTAPI_LOCAL_URL = "http://127.0.0.1:8002/chatbot"


# Django -> FastAPI 호출
@csrf_exempt
def sales_chatbot(request):
    # sales_chatbot 요청을 받았을 때 사용자가 볼 첫 화면이 sales_chatbot.html
    if request.method == 'GET':
        return render(request, 'sales/sales_chatbot.html')

    # '보내기' 버튼 누르면 POST 요청. 사용자 질문을 json으로 FastAPI에 전달
    if request.method == 'POST':
        try:
            # 프론트엔드가 사용자가 입력한 질문을 Django로 보내고,
            # 이 데이터를 request.body가 json 형식의 문자열로 받고, json.loads가 파이썬 딕셔너리로 변환
            data = json.loads(request.body)
            user_question = data.get("question", "")  # 사용자 질문 내용을 user_question에 저장

            # 현재 로그인한 사용자의 store 가져오기
            if hasattr(request.user, "member") and request.user.member and request.user.member.store:
                store = request.user.member.store  # 로그인한 사용자의 매장 정보
            else:
                return JsonResponse({"error": "매장 정보가 없습니다."}, status=400)

            # 매장별 데이터 가져오기
            sales_data = get_sales_data(store)

            # FastAPI 요청
            response = requests.post(
                FASTAPI_LOCAL_URL,
                headers={'Content-Type': 'application/json'},
                json={"question": user_question, "sales_data": sales_data},
                timeout=60
            )

            # FastAPI 응답 처리
            if response.status_code == 200:
                result = response.json()  # json 형식으로 result에 저장

                # tts 파일 url (상대경로 -> 절대경로)
                if result.get('tts_file') and not result['tts_file'].startswith('http'):
                    result['tts_file'] = f"http://127.0.0.1:8001{result['tts_file']}"

                return JsonResponse(result)
            else:
                error_msg = f"FastAPI 서버 오류: {response.status_code}"
                return JsonResponse({'error': error_msg}, status=500)

        # 오류 발생 시 발생한 오류 객체를 e에 넣고, e를 json 형식으로 변환하기 위해 str에 감싸서 JsonResponse 처리
        except Exception as e:
            error_msg = f"요청 처리 중 오류: {str(e)}"
            return JsonResponse({"error": error_msg}, status=500)

    error_msg = "지원하지 않는 요청 방식입니다."
    return JsonResponse({"error": error_msg}, status=405)


# DB - 제품별 매출 데이터 조회
def get_sales_data(store):
    try:
        now_time = now()
        today = now_time.date()
        start_7d = today - timedelta(days=7)
        start_30d = today - timedelta(days=30)
        yesterday = today - timedelta(days=1)

        # 제품별 매출 데이터
        product_sales = {}

        # 매장별 주문 데이터 조회
        orders = OrderInfo.objects.filter(store=store)

        # 기간별 매출액&판매량
        sales_summary = {
            "today_sales": 0, "today_count": 0,
            "yesterday_sales": 0, "yesterday_count": 0,
            "sales_7d": 0, "count_7d": 0,
            "sales_30d": 0, "count_30d": 0
        }

        for order in orders:
            order_datetime = order.order_at
            order_date = order.order_at.date()
            order_items = OrderItem.objects.filter(order=order)

            # 주문별 총 매출액&판매량
            order_total = order.total_amount
            order_count = order.total_count

            # 기간별 매장 총 매출액&판매량
            if order_date == today:  # 오늘 매출
                sales_summary["today_sales"] += order_total
                sales_summary["today_count"] += order_count

            if order_date == yesterday:  # 어제 매출
                sales_summary["yesterday_sales"] += order_total
                sales_summary["yesterday_count"] += order_count

            if start_7d <= order_date <= today:  # 최근 7일 매출
                sales_summary["sales_7d"] += order_total
                sales_summary["count_7d"] += order_count

            if start_30d <= order_date <= today:  # 최근 30일 매출
                sales_summary["sales_30d"] += order_total
                sales_summary["count_30d"] += order_count

            # 개별 제품 매출
            for item in order_items:
                if item.item is None:
                    continue

                try:
                    product_id = item.item.item_id
                    product_name = item.item.item_name
                    category = item.item.category
                except AttributeError:
                    continue

                # 개별 제품 매출액 및 판매량
                revenue = item.item_total
                count = item.item_count

                if product_id not in product_sales:  # 처음 등장하는 제품인지 확인
                    # 새 제품 정보 초기화
                    product_sales[product_id] = {
                        "product_id": product_id,
                        "product_name": product_name,
                        "category": category,
                        "today_sales": 0,
                        "today_count": 0,
                        "yesterday_sales": 0,
                        "yesterday_count": 0,
                        "sales_7d": 0,
                        "count_7d": 0,
                        "sales_30d": 0,
                        "count_30d": 0
                    }

                # 기간별 제품 총 매출액&판매량
                if order_date == today:  # 오늘 매출
                    product_sales[product_id]["today_sales"] += revenue
                    product_sales[product_id]["today_count"] += count

                if order_date == yesterday:  # 어제 매출
                    product_sales[product_id]["yesterday_sales"] += revenue
                    product_sales[product_id]["yesterday_count"] += count

                if start_7d <= order_date <= today:  # 최근 7일 매출
                    product_sales[product_id]["sales_7d"] += revenue
                    product_sales[product_id]["count_7d"] += count

                if start_30d <= order_date <= today:  # 최근 30일 매출
                    product_sales[product_id]["sales_30d"] += revenue
                    product_sales[product_id]["count_30d"] += count

        return {
            "products": list(product_sales.values()),
            "summary": sales_summary
        }
    except Exception as e:
        print(f"데이터 로딩 오류: {e}")
        return {"products": [], "summary": {}}