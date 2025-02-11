from django.shortcuts import render

def kiosk_main(request):
    return render(request, 'kiosk/kiosk_main.html')  # kiosk_main 템플릿 파일 경로 지정

def products(request):
    return render(request, 'kiosk/kiosk_products.html')  # kiosk_상품안내화면 템플릿 파일 경로 지정

def member(request):
    return render(request, 'kiosk/kiosk_member.html')  # kiosk_회원확인 템플릿 파일 경로 지정

def point(request):
    return render(request, 'kiosk/kiosk_point.html')  # kiosk_포인트 적립 템플릿 파일 경로 지정

def usepoint(request):
    return render(request, 'kiosk/kiosk_usepoint.html')  # kiosk_포인트 사용 템플릿 파일 경로 지정

def payment_method(request):
    return render(request, 'kiosk/kiosk_payment_method.html')  # kiosk_결제방식 템플릿 파일 경로 지정


