from django.shortcuts import render


def pay_main(request):
    # purchases = Purchase.objects.all().order_by('-date')
    return render(request, 'pay/pay_main.html')  # 템플릿 파일 경로 지정
    # return render(request, 'pay/pay_main.html', {'purchases': purchases})

def pay_details(request):
    return render(request, 'pay/pay_details.html')
    # payment = Purchase.objects.get(id=payment_id)
    # return render(request, 'pay_details.html', {'payment': payment})

def pay_cancel(request):
    return render(request, 'pay/pay_cancel.html')
