from django.shortcuts import render

def menu_main(request):
    return render(request, '../templates/menu/menu_main.html')  # 템플릿 파일 경로 지정
