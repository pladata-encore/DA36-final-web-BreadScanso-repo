from django.shortcuts import render
from django.http import JsonResponse
from member.models import Member
from django.views.decorators.csrf import csrf_exempt
from menu.models import Item
from .models import OrderInfo, PaymentInfo, OrderItem  # OrderItem 추가
from django.utils import timezone
import json


def kiosk_main(request):
    return render(request, 'kiosk/kiosk_main.html')

def products(request):
    items = Item.objects.values('item_name', 'item_name_eng', 'sale_price')
    menu_dict = {item['item_name_eng']: {
        'name': item['item_name'],
        'price': item['sale_price']
    } for item in items}

    return render(request, 'kiosk/kiosk_products.html', {
        'menu_data': menu_dict
    })

def member(request):
    return render(request, 'kiosk/kiosk_member.html')

def phonenumber(request):
    return render(request, 'kiosk/kiosk_phonenumber.html')

def usepoint(request):
    return render(request, 'kiosk/kiosk_usepoint.html')

def payment_method(request):
    return render(request, 'kiosk/kiosk_payment_method.html')

def payment_completed(request):
    return render(request, 'kiosk/kiosk_payment_completed.html')


def check_phone_number(request):
    phone_num = request.GET.get("phone_num")

    if not phone_num:
        return JsonResponse({"is_member": False, "message": "전화번호가 제공되지 않았습니다."})

    try:
        member = Member.objects.filter(phone_num=phone_num).first()

        if member:
            return JsonResponse({
                "is_member": True,
                "phone_num": member.phone_num,
                "points": member.points
            })
        else:
            return JsonResponse({"is_member": False, "message": "회원이 아닙니다."})

    except Exception as e:
        return JsonResponse({"is_member": False, "error": str(e)})


@csrf_exempt
def update_points(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_num = data.get("phone_num")
            final_points = data.get("final_points")
            final_amount = data.get("final_amount", 0)  # 최종 결제 금액 추가

            if not phone_num or final_points is None:
                return JsonResponse({"success": False, "message": "필수 데이터가 부족합니다."}, status=400)

            # 회원 정보 조회 및 업데이트
            member = Member.objects.filter(phone_num=phone_num).first()
            if member:
                member.points = final_points  # 포인트 업데이트
                member.total_spent += final_amount  # 총 지출 업데이트
                member.last_visited = timezone.now()  # 마지막 방문일 업데이트
                member.visit_count += 1  # 방문 횟수 업데이트
                member.save()
                return JsonResponse({"success": True, "message": "회원 정보가 업데이트되었습니다."})
            else:
                return JsonResponse({"success": False, "message": "해당 회원을 찾을 수 없습니다."}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "잘못된 JSON 형식입니다."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "잘못된 요청 방식입니다."}, status=405)


@csrf_exempt
def complete_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_num = data.get("phone_num", "")  # 기본값을 빈 문자열로 설정
            total_amount = data.get("final_amount")  # 총 결제 금액
            used_points = data.get("used_points", 0)  # 사용 포인트 추가
            payment_method = data.get("payment_method", "credit")
            products = data.get("products", {})

            # total_amount만 필수로 체크
            if not total_amount:
                return JsonResponse({"success": False, "message": "결제 금액이 필요합니다."}, status=400)

            # 회원 정보 조회 (비회원은 None)
            member = None
            if phone_num:
                member = Member.objects.filter(phone_num=phone_num).first()

            # OrderInfo 생성
            order = OrderInfo.objects.create(
                total_amount=total_amount,
                store=request.session.get('store', 'A')
            )

            # 최종 결제 금액 계산 (포인트 사용 적용)
            order.calculate_final_amount(used_points)

            # 적립 포인트 계산
            earned_points = order.calculate_earned_points()

            # 변경사항 저장
            order.save()

            # OrderItem 생성
            for product_name, product_data in products.items():
                try:
                    item = Item.objects.filter(
                        item_name_eng=product_name,
                        store=request.session.get('store')
                    ).first()
                    OrderItem.objects.create(
                        order=order,
                        item=item,
                        item_count=product_data.get('quantity', 0),
                        item_price=product_data.get('price', 0),
                        item_total=product_data.get('totalAmount', 0)
                    )
                except Item.DoesNotExist:
                    continue

            # PaymentInfo 생성
            payment = PaymentInfo.objects.create(
                order=order,
                member=member,  # 비회원은 None
                payment_method=payment_method,
                used_points=used_points  # 사용 포인트 저장
            )

            return JsonResponse({
                "success": True,
                "message": "결제가 완료되었습니다.",
                "order_id": order.order_id,
                "payment_id": payment.payment_id,
                "earned_points": order.earned_points  # 적립 포인트 반환
            })

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "잘못된 JSON 형식입니다."}, status=400)
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)}, status=500)

    return JsonResponse({"success": False, "message": "잘못된 요청 방식입니다."}, status=405)