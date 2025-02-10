from django.shortcuts import render

def store_info_main(request):
    return render(request, '../templates/store_info/store_info_main.html')  # 템플릿 파일 경로 지정