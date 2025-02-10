from django.shortcuts import render

def kiosk_main(request):
    return render(request, '../templates/kiosk/kiosk_main.html')  # 템플릿 파일 경로 지정
