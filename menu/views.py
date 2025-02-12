from django.shortcuts import render

def menu_main(request):
    return render(request, 'menu/menu_main.html')  # 메인에서 메뉴정보 경로

def menu_store(request):
    return render(request, 'menu/menu_store.html')  # 점주 페이지의 메뉴관리 경로

def product_detail(request, product_id):
    return render(request, 'menu/product_detail.html', {'product_id': product_id}) # 제품상세 페이지 경로

def menu_main_bread(request):
    return render(request, 'menu/menu_main_bread.html') # 빵 카테고리 경로 #TODO 이후 product_category 로 경로 불러오게 할지 고민중

def menu_main_dessert(request):
    return render(request, 'menu/menu_main_dessert.html') # 디저트 카테고리 경로 #TODO 이후 product_category 로 경로 불러오게 할지 고민중
