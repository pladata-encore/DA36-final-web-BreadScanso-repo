from django.shortcuts import render

def store_main(request):
    return render(request, '../templates/store/store_main.html')  # 템플릿 파일 경로 지정
