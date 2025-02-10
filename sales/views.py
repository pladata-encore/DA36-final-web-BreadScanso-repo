from django.shortcuts import render

def sales_main(request):
    return render(request, '../templates/sales/sales_main.html')  # 템플릿 파일 경로 지정
