from django.shortcuts import render

def stock_main(request):
    return render(request, '../templates/stock/stock_main.html')  # 템플릿 파일 경로 지정
