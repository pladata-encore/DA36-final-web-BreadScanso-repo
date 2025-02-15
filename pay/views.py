from django.shortcuts import render, get_object_or_404
# from .models import Purchase

def pay_main(request):
    # purchases = Purchase.objects.all().order_by("-date")
    #
    # payment_filter = request.GET.get("payment_method")
    # if payment_filter:
    #     purchases = purchases.filter(payment_method=payment_filter)
    return render(request, "pay/pay_main.html")
    # return render(request, "pay/pay_main.html", {"purchases": purchases})


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
    # purchases = Purchase.objects.filter(member_status="member", is_cancelled=False).order_by("-date")
    # return render(request, "pay/pay_member.html", {"purchases": purchases})
    return render(request, "pay/pay_member.html")

def pay_member_details(request):
# def pay_member_details(request, payment_id):
#     purchase = get_object_or_404(Purchase, id=payment_id, member_status="member")
    return render(request, 'pay/pay_member_details.html')
    # return render(request, 'pay/pay_member_details.html', {'purchase': purchase})

def pay_member_cancel(request):
    # cancels = Purchase.objects.filter(member_status="member", is_cancelled=True).order_by("-date")
    # return render(request, "pay/pay_member_cancel.html", {"cancels": cancels})
    return render(request, "pay/pay_member_cancel.html")
