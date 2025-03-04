from django.shortcuts import render
from django.http import JsonResponse
from member.models import Member
from django.views.decorators.csrf import csrf_exempt
from menu.models import Item
from .models import OrderInfo, PaymentInfo, OrderItem  # OrderItem 추가
from django.utils import timezone
import json
from django.db import transaction


def kiosk_main(request):
    return render(request, 'kiosk/kiosk_main.html')

def products(request):
    store = request.session.get('store')

    # store 값이 없으면 빈 dictionary로 반환
    if not store:
        menu_dict = {}
    else:
        # store 값에 해당하는 항목만 필터링
        items = Item.objects.filter(store=store).values('item_name', 'item_name_eng', 'sale_price', 'item_id')

        menu_dict = {item['item_name_eng']: {
            'name': item['item_name'],
            'price': item['sale_price'],
            'item_id': item['item_id']
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
def complete_payment(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            phone_num = data.get("phone_num", "")
            final_amount = data.get("final_amount")
            used_points = data.get("used_points", 0)
            points = data.get("points", 0)
            earned_points = data.get("earned_points", 0)
            payment_method = data.get("payment_method", "credit")
            products = data.get("products", {})

            print("디버깅 - 요청 데이터:")
            print(f"전화번호: {phone_num}")
            print(f"결제 금액: {final_amount}")
            print(f"사용한 포인트: {used_points}")
            print(f"총 포인트: {points}")
            print(f"적립된 포인트: {earned_points}")
            print(f"결제 방식: {payment_method}")
            print(f"상품 데이터: {products}")


            if not final_amount or final_amount < 0:
                return JsonResponse({"success": False, "message": "결제 금액이 필요합니다."}, status=400)

            # 회원 정보 조회 및 업데이트 (update_points 기능)
            member = Member.objects.filter(phone_num=phone_num).first() if phone_num else None

            if member and phone_num:
                member.total_spent += final_amount  # 총 지출 업데이트
                member.last_visited = timezone.now()  # 마지막 방문일 업데이트
                member.visit_count += 1  # 방문 횟수 업데이트
                member.points = points  # 포인트 업데이트
                member.save()

            with transaction.atomic():
                # OrderItem 합계로 total_amount 계산
                order = OrderInfo.objects.create(
                    store=request.session.get('store', 'A'),
                    used_points=used_points,
                    earned_points=earned_points,
                    final_amount=final_amount
                )

                total_amount = 0
                for product_name, product_data in products.items():
                    # 1. item_id가 있으면 직접 사용
                    if 'item_id' in product_data and product_data['item_id']:
                        item = Item.objects.filter(item_id=product_data['item_id']).first()
                    # 2. 없으면 item_name_eng로 검색
                    else:
                        item = Item.objects.filter(item_name_eng=product_name, store=order.store).first()

                    if item:
                        # totalPrice 필드 사용
                        order_item = OrderItem.objects.create(
                            order=order,
                            item=item,
                            item_count=product_data.get('quantity', 0),
                            item_price=product_data.get('price', 0),
                            item_total=product_data.get('totalPrice', 0)  # totalAmount → totalPrice로 수정
                        )
                        total_amount += order_item.item_total
                    else:
                        # 디버깅용: 아이템을 찾지 못했을 때 로그 기록
                        print(f"상품을 찾을 수 없음: {product_name}, 데이터: {product_data}")

                order.total_amount = total_amount
                order.save()

                payment = PaymentInfo.objects.create(
                    order=order,
                    member=member,
                    payment_method=payment_method,
                    used_points=used_points
                )

            return JsonResponse({
                "success": True,
                "message": "결제가 완료되었습니다.",
                "order_id": order.order_id,
                "payment_id": payment.payment_id,
            })
        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "잘못된 JSON 형식입니다."}, status=400)
        except Exception as e:
            # 디버깅용: 예외 자세히 기록
            import traceback
            print(traceback.format_exc())
            return JsonResponse({"success": False, "message": str(e)}, status=500)
    return JsonResponse({"success": False, "message": "잘못된 요청 방식입니다."}, status=405)