from django.shortcuts import render

def pay_main(request):
    return render(request, 'pay/pay_main.html')  # 템플릿 파일 경로 지정

def pay_details(request):
    return render(request, 'pay/pay_details.html')

def pay_cancel(request):
    return render(request, 'pay/pay_cancel.html')