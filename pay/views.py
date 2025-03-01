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

    # 결제 내역에 '취소' 여부 추가
    for payment in payment_infos:
        payment.is_canceled = not payment.payment_status

    # 페이지네이션 (10개씩 표시)
    paginator = Paginator(payment_infos, 10)  # 한 페이지당 10개씩
    page_number = request.GET.get("page")  # 현재 페이지 번호 가져오기

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)  # 유효하지 않은 페이지 번호라면 첫 페이지로 이동

    return render(request, "pay/pay_main.html", {"member": member, "page_obj": page_obj})

def pay_cancel(request):

    member = request.user.member
    store = member.store if member.member_type == "manager" else None
    payment_method = request.GET.get("payment_method")
    if store:
        canceled_payments = PaymentInfo.objects.filter(order__store=store, payment_status=False).order_by("-pay_at")

        if payment_method in ["credit", "epay"]:
            canceled_payments = canceled_payments.filter(payment_method=payment_method)
    else:
        canceled_payments = PaymentInfo.objects.none()

    paginator = Paginator(canceled_payments, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    return render(request, "pay/pay_cancel.html", {"member": member, "page_obj": page_obj, "canceled_payments": canceled_payments})

def pay_details(request, payment_id):
    payment = get_object_or_404(PaymentInfo, pk=payment_id)

    # 결제한 매장의 매니저 (store_owner)
    store_owner = Member.objects.filter(store=payment.order.store, member_type="manager").first()

    return render(request, 'pay/pay_details.html', {
        'payment': payment,
        'store_owner': store_owner
    })

def pay_member(request):
    member = request.user.member  # 로그인한 회원 정보 가져오기

    # 현재 로그인한 회원(member_id) 기준으로 결제 내역 조회
    member_payments = PaymentInfo.objects.filter(member=member).order_by("-pay_at")

    # 결제수단 필터링
    payment_method = request.GET.get("payment_method")
    if payment_method in ["credit", "epay"]:
        member_payments = member_payments.filter(payment_method=payment_method)

    # 결제 내역에 '취소' 여부 추가
    for payment in member_payments:
        payment.is_canceled = not payment.payment_status

    # 페이지네이션 (10개씩 표시)
    paginator = Paginator(member_payments, 10)  # 한 페이지당 10개씩
    page_number = request.GET.get("page")  # 현재 페이지 번호 가져오기

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)  # 유효하지 않은 페이지 번호라면 첫 페이지로 이동

    return render(request, "pay/pay_member.html", {"member": member, "page_obj": page_obj})

def pay_member_details(request, payment_id):
    payment = get_object_or_404(PaymentInfo, pk=payment_id, member=request.user.member)

    store_owner = Member.objects.filter(store__iexact=payment.order.store, member_type="manager").first()

    if store_owner is None:
        store_owner = {"name": "정보 없음", "store_num": "정보 없음"}

    return render(request, 'pay/pay_member_details.html', {
        'payment': payment,
        'store_owner': store_owner
    })


def pay_member_cancel(request):
    member = request.user.member
    payment_method = request.GET.get("payment_method")

    # 현재 로그인한 회원(member_id) 기준 결제 취소 내역 조회
    canceled_payments = PaymentInfo.objects.filter(member=member, payment_status=False).order_by("-pay_at")

    # 결제수단 필터링 추가
    if payment_method in ["credit", "epay"]:
        canceled_payments = canceled_payments.filter(payment_method=payment_method)

    paginator = Paginator(canceled_payments, 10)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.get_page(page_number)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.get_page(1)

    return render(request, "pay/pay_member_cancel.html", {"member": member, "page_obj": page_obj})



