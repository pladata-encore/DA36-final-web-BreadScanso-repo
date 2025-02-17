from django.shortcuts import render
from .models import Item

def menu_main(request):
    return render(request, 'menu/menu_main.html')  # 메인 메뉴정보 페이지

def menu_store(request):
    items = Item.objects.all()
    return render(request, 'menu/menu_store.html', {'items': items})  # 점주 페이지의 메뉴관리 페이지

def product_detail(request, product_id):
    return render(request, 'menu/product_detail.html', {'product_id': product_id}) # 제품상세 페이지 경로

def menu_main_bread(request):
    return render(request, 'menu/menu_main_bread.html') # 빵 카테고리 페이지 #TODO 이후 product_category 로 경로 불러오게 할지 고민중

def menu_main_dessert(request):
    return render(request, 'menu/menu_main_dessert.html') # 디저트 카테고리 페이지 #TODO 이후 product_category 로 경로 불러오게 할지 고민중

def menu_store_new_menu(request):
    return render(request, 'menu/new_menu.html') # 점주 신규 메뉴 등록 페이지

def menu_store_menu_info(request):
    return render(request, 'menu/menu_info.html') # 점주 메뉴관리 상세 페이지

def menu_store_menu_edit(request):
    return render(request, 'menu/menu_edit.html') # 점주 메뉴관리 수정 페이지