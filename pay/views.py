from django.shortcuts import render, get_object_or_404
from kiosk.models import PaymentInfo
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from member.models import Member


def kiosk_main(request):
    return render(request, 'kiosk/kiosk_main.html')  # kiosk_main 템플릿 파일 경로 지정


def pay_main(request):
    member = request.user.member

    # 로그인한 사용자의 store 값 가져오기
    store = member.store if member.member_type == "manager" else None

    # 결제수단
    payment_method = request.GET.get("payment_method")

    # 해당 store의 결제 내역 가져오기 (store가 없으면 빈 쿼리셋 반환)
    if store:
        payment_infos = PaymentInfo.objects.filter(order__store=store).order_by("-pay_at")
        # 결제수단 - 토글
        if payment_method in ["credit", "epay"]:
            payment_infos = payment_infos.filter(payment_method=payment_method)
    else:
        payment_infos = PaymentInfo.objects.none()  # 안전하게 빈 쿼리셋 반환

    # 페이지네이션 (10개씩 표시)
    paginator = Paginator(payment_infos, 10)  # 한 페이지당 10개씩
    page_number = request.GET.get("page")  # 현재 페이지 번호 가져오기

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)  # 유효하지 않은 페이지 번호라면 첫 페이지로 이동

    return render(request, "pay/pay_main.html", {"member": member, "page_obj": page_obj})


# def pay_details(request, payment_id):
# def pay_details(request):
#     # payment = get_object_or_404(Purchase, id=payment_id)
#     return render(request, 'pay/pay_details.html')
#     # return render(request, 'pay/pay_details.html', {'payment': payment})

def pay_details(request, payment_id):
    payment = get_object_or_404(PaymentInfo, pk=payment_id)

    # 결제한 매장의 대표자 가져오기 (변수명 변경: store_owner)
    store_owner = Member.objects.filter(store=payment.order.store, member_type="manager").first()

    return render(request, 'pay/pay_details.html', {
        'payment': payment,
        'store_owner': store_owner
    })


# def pay_cancel(request):
#     # cancels = Purchase.objects.filter(is_cancelled=True).order_by("-date")
#     # GET 요청 처리 (member 데이터 가져오기)
#     member = request.user.member
#
#     return render(request, 'pay/pay_cancel.html', {"member": member})
#     # return render(request, "pay/pay_cancel.html", {"cancels": cancels})

def pay_cancel(request):
    member = request.user.member
    store = member.store if member.member_type == "manager" else None

    # 취소된 결제 내역 가져오기 (payment_status=False)
    if store:
        canceled_payments = PaymentInfo.objects.filter(order__store=store, payment_status=False).order_by("-pay_at")
    else:
        canceled_payments = []

    return render(request, "pay/pay_cancel.html", {"member": member, "cancels": canceled_payments})


def pay_member(request):
    # GET 요청 처리
    member = request.user.member
    return render(request, "pay/pay_member.html", {'member': member})

def pay_member_details(request):
# def pay_member_details(request, payment_id):
#     purchase = get_object_or_404(Purchase, id=payment_id, member_status="member")
    return render(request, 'pay/pay_member_details.html')
    # return render(request, 'pay/pay_member_details.html', {'purchase': purchase})

def pay_member_cancel(request):
    # cancels = Purchase.objects.filter(member_status="member", is_cancelled=True).order_by("-date")
    # return render(request, "pay/pay_member_cancel.html", {"cancels": cancels})
    member = request.user.member

    return render(request, "pay/pay_member_cancel.html", {'member': member})


