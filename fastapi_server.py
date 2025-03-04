from fastapi import FastAPI
from pydantic import BaseModel
import os
import requests
from fastapi.middleware.cors import CORSMiddleware
from gtts import gTTS
import time
from fastapi.responses import FileResponse
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI()

# OpenAI API 키 가져오기
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# TTS 파일 저장 경로
TTS_SAVE_PATH = "static/tts"


# ChatRequest : FastAPI가 데이터가 올바른지 자동으로 확인하게 하는 모델
class ChatRequest(BaseModel):
    question: str  # user의 질문은 str 타입
    sales_data: dict  # django에서 가져온 매출데이터는 dict 타입


# django -> FastAPI 호출
# 챗봇 엔드포인트
@app.post("/chatbot")  # django가 /chatbot 엔드포인트로 POST 요청
async def chatbot_endpoint(request: ChatRequest):  # request가 ChatRequest 타입이므로, question, sales_data 자동 파싱
    try:
        if not request.question:
            return {"error": "질문을 입력해 주세요."}

        # 매출 데이터 검증
        if not request.sales_data:
            print("매출 데이터가 없습니다.")
            # 빈 데이터라도 에러가 나지 않게 기본값 설정
            request.sales_data = {"products": [], "summary": {}}

        # 비동기로 django_chatbot 호출 -> OpenAPI 요청 끝날 떄까지 기다려서 응답 반환
        return await django_chatbot(request)

    except Exception as e:
        print(f"서버오류: {str(e)}")
        return {"error": f"서버오류: {str(e)}"}


# OpenAI API 호출 -> AI 응답 생성
async def django_chatbot(request: ChatRequest):
    try:
        # 사용자 질문 + 매출데이터를 하나의 프롬프트로 변환
        prompt = generate_prompt(request.question, request.sales_data)
        # openai API에 프롬프트 보내서 답변 받음
        openai_response = get_openai_response(prompt)
        # TTS 변환 / 변환 실패 시 None
        tts_file = generate_tts(openai_response) if openai_response else None
        # AI 응답, tts 파일 경로 반환
        return {"answer": openai_response, "tts_file": tts_file}
    except Exception as e:
        print(f"OpenAI API 오류: {str(e)}")
        return {"error": f"OpenAI API 오류: {str(e)}"}


# 사용자 질문, 매출 데이터 프롬프트
def generate_prompt(question, sales_data):
    # 매장 총 매출 요약
    summary = sales_data.get("summary", {})

    # 안전하게 딕셔너리 접근
    total_sales_info = f"""
    - Today's Total Sales (Until Now): {summary.get('today_sales', 0)} KRW
    - Today's Total Units Sold (Until Now): {summary.get('today_count', 0)} units
    - Yesterday's Total Sales: {summary.get('yesterday_sales', 0)} KRW
    - Yesterday's Total Units Sold: {summary.get('yesterday_count', 0)} units
    - Recent 7 Days Total Sales: {summary.get('sales_7d', 0)} KRW
    - Recent 7 Days Total Units Sold: {summary.get('count_7d', 0)} units
    - Recent 30 Days Total Sales: {summary.get('sales_30d', 0)} KRW
    - Recent 30 Days Total Units Sold: {summary.get('count_30d', 0)} units
    """

    # 제품별 매출 데이터 - 안전하게 접근
    products = sales_data.get("products", [])
    product_sales_info = ""

    for product in products:
        if isinstance(product, dict):  # 제품이 딕셔너리인지 확인
            product_info = f"- {product.get('product_name', 'Unknown')} (ID: {product.get('product_id', 'Unknown')}): " + \
                           f"Today's sales (Until Now): {product.get('today_sales', 0)} KRW, " + \
                           f"Recent 7 days sales: {product.get('sales_7d', 0)} KRW, " + \
                           f"Recent 30 days sales: {product.get('sales_30d', 0)} KRW, " + \
                           f"Yesterday sales: {product.get('yesterday_sales', 0)} KRW, " + \
                           f"Today's units sold (Until Now): {product.get('today_count', 0)} units, " + \
                           f"Recent 7 days units sold: {product.get('count_7d', 0)} units, " + \
                           f"Recent 30 days units sold: {product.get('count_30d', 0)} units, " + \
                           f"Yesterday units sold: {product.get('yesterday_count', 0)} units"
            product_sales_info += product_info + "\n"

    return f"""
    You are an AI expert in bakery sales analysis.

    User's question: "{question}"

    🏪 Store Sales Summary:
    {total_sales_info}

    🍞 Product Sales Data:
    {product_sales_info}

    Based on the above data, please provide a detailed answer to the user's question.
    Answer in Korean language.
    """


# OpenAI API 요청 -> 챗봇 응답 가져오기
def get_openai_response(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": "You are an AI expert in bakery sales analysis."},
                {"role": "user", "content": prompt}
            ]
        }

        # OpenAI API에 데이터 보냄
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=60
        )

        # 응답 상태 코드 확인
        if response.status_code == 200:
            # JSON 응답 파싱
            result = response.json()

            # 안전하게 응답 데이터 추출
            if "choices" in result and len(result["choices"]) > 0:
                if "message" in result["choices"][0] and "content" in result["choices"][0]["message"]:
                    return result["choices"][0]["message"]["content"]
                else:
                    return "OpenAI 응답 구조 오류: 'message' 또는 'content' 키를 찾을 수 없습니다."
            else:
                return "OpenAI 응답 구조 오류: 'choices' 키를 찾을 수 없거나 비어 있습니다."
        else:
            return f"OpenAI API 오류: 상태 코드 {response.status_code}, 응답: {response.text}"

    except Exception as e:
        return f"OpenAI API 오류: {str(e)}"


# TTS
def generate_tts(text):
    try:
        if not os.path.exists(TTS_SAVE_PATH):
            os.makedirs(TTS_SAVE_PATH)  # 디렉토리 생성

        tts = gTTS(text=text, lang="ko")
        file_name = f"tts_{int(time.time())}.mp3"
        file_path = os.path.join(TTS_SAVE_PATH, file_name)

        tts.save(file_path)
        # 상대 URL 경로 반환
        return f"/tts/{file_name}"
    except Exception as e:
        print(f"TTS 변환 오류: {str(e)}")
        return None


# TTS 파일 제공 엔드포인트
# 생성된 파일 다운로드 / 브라우저에서 음성 재생
@app.get("/tts/{file_name}")
async def get_tts_file(file_name: str):
    file_path = os.path.join(TTS_SAVE_PATH, file_name)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mpeg", filename=file_name)
    return {"error": "파일을 찾을 수 없습니다."}


# Uvicorn 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run("fastapi_server:app", host="0.0.0.0", port=8002, reload=True)