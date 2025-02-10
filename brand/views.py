from django.shortcuts import render

def brand_main(request):
    return render(request, '../templates/brand/brand_main.html')  # 템플릿 파일 경로 지정
