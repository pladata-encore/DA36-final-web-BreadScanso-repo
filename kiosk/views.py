from django.shortcuts import render
from django.http import JsonResponse
from member.models import Member


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

def payment_completed(request):
    return render(request, 'kiosk/kiosk_payment_completed.html')  # kiosk_결제완료/영수증 템플릿 파일 경로 지정


def check_phone_number(request):
    phone_num = request.GET.get("phone_num")  # GET 방식으로 전화번호 받기

    if phone_num:
        # 회원이 존재하는지 확인
        exists = Member.objects.filter(phone_num=phone_num).exists()
        return JsonResponse({"is_member": exists})
    else:
        return JsonResponse({"is_member": False})

