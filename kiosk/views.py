from django.shortcuts import render

def kiosk_main(request):
    return render(request, '../templates/kiosk/kiosk_main.html')  # kiosk_main 템플릿 파일 경로 지정

def products(request):
    return render(request, '../templates/kiosk/kiosk_products.html')  # kiosk_상품안내화면 템플릿 파일 경로 지정

def member(request):
    return render(request, '../templates/kiosk/kiosk_member.html')  # kiosk_회원확인 템플릿 파일 경로 지정

