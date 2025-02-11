from django.shortcuts import render

def menu_main(request):
    return render(request, 'menu/menu_main.html')  # 메인에서 메뉴정보 경로

def menu_store(request):
    return render(request, 'menu/menu_store.html')  # 점주 페이지의 메뉴관리 경로

