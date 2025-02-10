from django.shortcuts import render

def pay_main(request):
    return render(request, '../templates/pay/pay_main.html')  # 템플릿 파일 경로 지정
