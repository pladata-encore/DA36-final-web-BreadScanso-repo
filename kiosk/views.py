from django.shortcuts import render
from django.http import JsonResponse
from member.models import Member


def kiosk_main(request):
    return render(request, 'kiosk/kiosk_main.html')  # kiosk_main 템플릿 파일 경로 지정

def products(request):
    return render(request, 'kiosk/kiosk_products.html')  # kiosk_상품안내화면 템플릿 파일 경로 지정

def member(request):
    return render(request, 'kiosk/kiosk_member.html')  # kiosk_회원확인 템플릿 파일 경로 지정

def phonenumber(request):
    return render(request, 'kiosk/kiosk_phonenumber.html')  # kiosk_전화번호 확인 템플릿 파일 경로 지정

def usepoint(request):
    return render(request, 'kiosk/kiosk_usepoint.html')  # kiosk_포인트 사용 템플릿 파일 경로 지정

def payment_method(request):
    return render(request, 'kiosk/kiosk_payment_method.html')  # kiosk_결제방식 템플릿 파일 경로 지정

def payment_completed(request):
    return render(request, 'kiosk/kiosk_payment_completed.html')  # kiosk_결제완료/영수증 템플릿 파일 경로 지정


def check_phone_number(request):
    phone_num = request.GET.get("phone_num")  # GET 방식으로 전화번호 받기

    if not phone_num:
        return JsonResponse({"is_member": False, "message": "전화번호가 제공되지 않았습니다."})

    try:
        # 회원 정보 조회
        member = Member.objects.filter(phone_num=phone_num).first()

        if member:
            return JsonResponse({
                "is_member": True,
                "phone_num": member.phone_num,  # 전화번호 반환
                "points": member.points  # 적립금 반환
            })
        else:
            return JsonResponse({"is_member": False, "message": "회원이 아닙니다."})

    except Exception as e:
        return JsonResponse({"is_member": False, "error": str(e)})


