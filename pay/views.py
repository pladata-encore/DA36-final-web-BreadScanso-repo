from django.shortcuts import render

def kiosk_main(request):
    return render(request, 'kiosk/kiosk_main.html')  # kiosk_main 템플릿 파일 경로 지정

def pay_main(request):
    return render(request, "pay/pay_main.html")


# def pay_details(request, payment_id):
def pay_details(request):
    # payment = get_object_or_404(Purchase, id=payment_id)
    return render(request, 'pay/pay_details.html')
    # return render(request, 'pay/pay_details.html', {'payment': payment})


def pay_cancel(request):
    # cancels = Purchase.objects.filter(is_cancelled=True).order_by("-date")
    return render(request, 'pay/pay_cancel.html')
    # return render(request, "pay/pay_cancel.html", {"cancels": cancels})

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
    return render(request, "pay/pay_member_cancel.html")


