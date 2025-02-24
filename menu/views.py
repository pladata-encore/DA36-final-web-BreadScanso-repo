import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Item, NutritionInfo, Allergy

def menu_main(request):
    items = Item.objects.filter(show='1')
    best_items = []  # best=1인 아이템을 저장할 리스트
    for item in items:
        item.image_filename = get_existing_image(item.item_name_eng)  # 존재하는 파일만 저장
        if item.best == 1 and item.show == 1:
            best_items.append(item)  # best 컬럼이 1인 아이템만 저장
    return render(request, 'menu/menu_main.html', {'items': items, 'best_items': best_items})  # 메인 메뉴정보 페이지

def menu_store(request):
    items = Item.objects.all()
    paginator = Paginator(items, 10)  # 한 페이지당 10개씩 표시
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, 'menu/menu_store.html',{'items': items, "page_obj": page_obj})  # 점주 페이지의 메뉴관리 페이지

def product_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)  # 해당 item_id의 제품을 가져옴
    item.image_filename = get_existing_image(item.item_name_eng)  # 존재하는 파일만 저장
    nutrition_info = NutritionInfo.objects.filter(item_id=item_id).first() # NutritionInfo에서 해당 item_id의 영양 정보 가져오기
    allergy_info = Allergy.objects.filter(item_id=item_id).first() # AllergyInfo에서 해당 item_id의 영양 정보 가져오기
    return render(request, 'menu/product_detail.html', {'item': item, 'nutrition': nutrition_info, 'allergy': allergy_info})  # 제품 상세 페이지 경로

def menu_main_bread(request):
    items = Item.objects.filter(category='bread', show=1)  # 'dessert' 카테고리이면서 show가 1인 항목만 필터링
    best_items = []  # best=1인 아이템을 저장할 리스트
    for item in items:
        item.image_filename = get_existing_image(item.item_name_eng)  # 존재하는 파일만 저장
        if item.best == 1 and item.show == 1:  # best 컬럼이 1이고 show가 1인 아이템만 저장
            best_items.append(item)  # best 컬럼이 1인 아이템만 저장
    return render(request, 'menu/menu_main_bread.html', {'items': items, 'best_items': best_items})  # 디저트 카테고리 페이지

def menu_main_dessert(request):
    items = Item.objects.filter(category='dessert', show=1)  # 'dessert' 카테고리이면서 show가 1인 항목만 필터링
    best_items = []  # best=1인 아이템을 저장할 리스트
    for item in items:
        item.image_filename = get_existing_image(item.item_name_eng)  # 존재하는 파일만 저장
        if item.best == 1 and item.show == 1:  # best 컬럼이 1이고 show가 1인 아이템만 저장
            best_items.append(item)  # best 컬럼이 1인 아이템만 저장
    return render(request, 'menu/menu_main_dessert.html', {'items': items, 'best_items': best_items})  # 디저트 카테고리 페이지

def menu_add(request):
    return render(request, 'menu/new_menu.html') # 점주 신규 메뉴 등록 페이지

def menu_store_menu_info(request):
    return render(request, 'menu/menu_info.html') # 점주 메뉴관리 상세 페이지

def menu_store_menu_edit(request):
    return render(request, 'menu/menu_edit.html') # 점주 메뉴관리 수정 페이지

# 메뉴 메인 제품정보 이미지 불러오기
def get_existing_image(item_name_eng):
    static_path = os.path.join(settings.STATICFILES_DIRS[0], 'images')
    for ext in ['.jpg', '.png']:
        file_path = os.path.join(static_path, f"{item_name_eng}{ext}")
        if os.path.exists(file_path):
            return f"{item_name_eng}{ext}"
    return None  # 이미지가 없으면 None 반환


@csrf_exempt  # POST 요청을 CSRF 검사 없이 받도록 설정 (테스트 용도)
def menu_save(request):
    if request.method == "POST":
        # 제품 기본 정보 저장
        item = Item.objects.create(
            item_name=request.POST.get("item_name"),
            category="bread" if request.POST.get("category") == "빵" else "dessert",
            description=request.POST.get("description"),
            cost_price=request.POST.get("cost_price"),
            sale_price=request.POST.get("sale_price"),
            best=bool(int(request.POST.get("best", 0))),
            new=bool(int(request.POST.get("new", 0))),
            show=bool(int(request.POST.get("show", 0)))
        )

        # 영양 정보 저장
        NutritionInfo.objects.create(
            item=item,
            nutrition_weight=request.POST.get("nutrition_weight"),
            nutrition_calories=request.POST.get("nutrition_calories"),
            nutrition_sodium=request.POST.get("nutrition_sodium"),
            nutrition_sugar=request.POST.get("nutrition_sugar"),
            nutrition_carbohydrates=request.POST.get("nutrition_carbohydrates"),
            nutrition_saturated_fat=request.POST.get("nutrition_saturated_fat"),
            nutrition_trans_fat=request.POST.get("nutrition_trans_fat"),
            nutrition_protein=request.POST.get("nutrition_protein")
        )

        # 알레르기 정보 저장
        Allergy.objects.create(
            item=item,
            allergy_wheat=bool(int(request.POST.get("allergy_wheat", 0))),
            allergy_milk=bool(int(request.POST.get("allergy_milk", 0))),
            allergy_egg=bool(int(request.POST.get("allergy_egg", 0))),
            allergy_soybean=bool(int(request.POST.get("allergy_soybean", 0))),
            allergy_nuts=bool(int(request.POST.get("allergy_nuts", 0))),
            allergy_etc=request.POST.get("allergy_etc", "")
        )

        return JsonResponse({"message": "메뉴가 성공적으로 저장되었습니다!", "item_id": item.id})

    return JsonResponse({"message": "잘못된 요청입니다."}, status=400)