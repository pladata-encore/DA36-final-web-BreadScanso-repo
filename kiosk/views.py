from django.shortcuts import render
from django.http import JsonResponse
from member.models import Member
from django.views.decorators.csrf import csrf_exempt
import json
from django.shortcuts import redirect



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



@csrf_exempt
def update_points(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # JSON 데이터 받기
            phone_num = data.get("phone_num")  # 전화번호 가져오기
            final_points = data.get("final_points")  # 최종 보유 포인트 가져오기

            if not phone_num or final_points is None:
                return JsonResponse({"success": False, "message": "필수 데이터가 부족합니다."}, status=400)

            # 회원 정보 조회 및 포인트 업데이트
            member = Member.objects.filter(phone_num=phone_num).first()
            if member:
                member.points = final_points  # 포인트 업데이트
                member.save()
                return JsonResponse({"success": True, "message": "포인트가 업데이트되었습니다."})
            else:
                return JsonResponse({"success": False, "message": "해당 회원을 찾을 수 없습니다."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "잘못된 JSON 형식입니다."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "잘못된 요청 방식입니다."}, status=405)



def reset_points(request):
    # 사용한 포인트를 0으로 설정하는 로직 추가
    request.session['used_points'] = 0  # 세션에 저장된 포인트 값 초기화

    # 'payment_method'로 리다이렉션
    return redirect('payment_method')

def reset_phonenumber(request):
    # 사용한 포인트를 0으로 설정하는 로직 추가
    request.session['phone_num'] = 0  # 세션에 저장된 포인트 값 초기화
    request.session['points'] = 0
    request.session['use_points'] = 0
    request.session['final_amount'] = 0
    request.session['earned_point'] = 0
    request.session['final_point'] = 0

    # 'payment_method'로 리다이렉션
    return redirect('payment_method')

