from django.shortcuts import render
import json
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv
import logging
import os

load_dotenv()
# FastAPI url 환경변수에서 로드
# FASTAPI_URL = os.getenv("FASTAPI_URL")
FASTAPI_LOCAL_URL = 'http://127.0.0.1:8003/chatbot'

# 로깅 설정
logger = logging.getLogger(__name__)

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

            print('user_question:', user_question)

            # 현재 로그인한 사용자의 store 가져오기
            if hasattr(request.user, "member") and request.user.member and request.user.member.store:
                store = request.user.member.store  # 로그인한 사용자의 매장 정보
            else:
                return JsonResponse({"error": "매장 정보가 없습니다."}, status=400)

            print('store:', store)
            # FastAPI 요청
            response = requests.post(
                # f"{FASTAPI_URL}/chatbot",
                FASTAPI_LOCAL_URL,
                headers={'Content-Type': 'application/json'},
                json={"question": user_question},
                timeout=60
            )
            print('response:', response)
            print(f"FastAPI 응답 상태 코드 : {response.status_code}")

            # FastAPI 응답 처리
            if response.status_code == 200:
                api_response = response.json()  # json 형식으로 result에 저장
                print(f"FastAPI 응답: {api_response}")
                return JsonResponse(api_response)
            else:
                error_msg = f"FastAPI 서버 오류: {response.status_code}"
                return JsonResponse({'error': error_msg}, status=500)

        # 오류 발생 시 발생한 오류 객체를 e에 넣고, e를 json 형식으로 변환하기 위해 str에 감싸서 JsonResponse 처리
        except Exception as e:
            print(e)
            error_msg = f"요청 처리 중 오류: {str(e)}"
            return JsonResponse({"error": error_msg}, status=500)

    error_msg = "지원하지 않는 요청 방식입니다."
    return JsonResponse({"error": error_msg}, status=405)