from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
import logging

# 로깅 설정
logger = logging.getLogger(__name__)

# 로깅 설정
logger = logging.getLogger(__name__)

FASTAPI_LOCAL_URL = "http://127.0.0.1:8002/chatbot"

@csrf_exempt
def sales_chatbot(request):
    if request.method == 'GET':
        return render(request, 'sales/sales_chatbot.html')

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_question = data.get("question", "")

            # FastAPI에 질문 전달
            response = requests.post(
                FASTAPI_LOCAL_URL,
                headers={'Content-Type': 'application/json'},
                json={"question": user_question},
                timeout=60
            )

            print(f"FastAPI 응답 상태 코드: {response.status_code}")

            if response.status_code == 200:
                api_response = response.json()
                print(f"FastAPI 응답 데이터: {api_response}")
                return JsonResponse(api_response)  # 비즈니스 어드바이저 응답 반환
            else:
                error_msg = f"FastAPI 오류: {response.status_code}"
                print(error_msg)
                if response.text:
                    print(f"오류 내용: {response.text}")
                return JsonResponse({'error': error_msg}, status=500)

        except Exception as e:
            error_msg = f"오류 발생: {str(e)}"
            print(error_msg)
            return JsonResponse({"error": error_msg}, status=500)

    return JsonResponse({"error": "지원하지 않는 요청 방식입니다."}, status=405)
