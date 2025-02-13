from django.shortcuts import render
from .models import Purchase

def pay_main(request):
    purchases = Purchase.objects.all().order_by('-date')
    return render(request, 'pay/pay_main.html', {'purchases': purchases})  # 템플릿 파일 경로 지정

def pay_details(request):
    return render(request, 'pay/pay_details.html')
    # payment = Purchase.objects.get(id=payment_id)
    # return render(request, 'pay_details.html', {'payment': payment})

def pay_cancel(request):
    return render(request, 'pay/pay_cancel.html')