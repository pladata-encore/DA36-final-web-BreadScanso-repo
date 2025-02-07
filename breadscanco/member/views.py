from django.http import HttpResponse
from django.shortcuts import render

# view.py 사용자의 요청을 처리하는 모듈
def index(request):
    print('index 함수 호출!')
    return HttpResponse("Hello world! This is Django login🎀")