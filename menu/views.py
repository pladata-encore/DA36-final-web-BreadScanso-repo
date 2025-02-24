import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Item, NutritionInfo, Allergy
import json

def menu_main(request):
    items = Item.objects.filter(show='1')
    best_items = []  # best=1인 아이템을 저장할 리스트
    for item in items:
        item.image_filename = get_existing_image(item.item_name_eng)  # 존재하는 파일만 저장
        if item.best == 1 and item.show == 1:
            best_items.append(item)  # best 컬럼이 1인 아이템만 저장
    return render(request, 'menu/menu_main.html', {'items': items, 'best_items': best_items})  # 메인 메뉴정보 페이지

def menu_store(request):
    items = Item.objects.all().order_by("item_id")
    # 페이지네이션 처리 (10개씩)
    paginator = Paginator(items, 10)
    # 페이지 번호 가져오기, 유효하지 않으면 1 페이지로 설정
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1
    try:
        page_obj = paginator.get_page(page_number)
    except EmptyPage:
        # 페이지 번호가 범위를 벗어난 경우 마지막 페이지로 설정
        page_obj = paginator.get_page(paginator.num_pages)
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

@require_http_methods(["POST"])
def menu_delete(request):
    try:
        # 요청 데이터 파싱
        data = json.loads(request.body)
        item_ids = data.get("item_ids", [])

        if not item_ids:
            return JsonResponse({
                "success": False,
                "message": "삭제할 항목이 없습니다."
            })

        NutritionInfo.objects.filter(item_id__in=item_ids).delete()
        Allergy.objects.filter(item_id__in=item_ids).delete()
        deleted_count, _ = Item.objects.filter(item_id__in=item_ids).delete()

        # 삭제 결과 반환
        if deleted_count > 0:
            return JsonResponse({
                "success": True,
            })
        else:
            return JsonResponse({
                "success": False,
            })

    except json.JSONDecodeError:
        return JsonResponse({
            "success": False,
            "message": "잘못된 요청 데이터입니다."
        })
    except Exception as e:
        return JsonResponse({
            "success": False,
            "message": "서버 오류가 발생했습니다."
        })


# 신규 제품 등록
def menu_save(request):
    if request.method == "POST":
        # best, new, show 체크박스 여부
        best = request.POST.get("best") == "on"
        new = request.POST.get("new") == "on"
        show = request.POST.get("show") == "on"

        # 기본 제품 정보
        item_name = request.POST.get("item_name")
        category = request.POST.get("category")
        store = request.POST.get("store")
        description = request.POST.get("description")
        cost_price = request.POST.get("cost_price")
        sale_price = request.POST.get("sale_price")

        # 영양 정보
        nutrition_weight = request.POST.get("nutrition_weight")
        nutrition_calories = request.POST.get("nutrition_calories")
        nutrition_sodium = request.POST.get("nutrition_sodium")
        nutrition_sugar = request.POST.get("nutrition_sugar")
        nutrition_carbohydrates = request.POST.get("nutrition_carbohydrates")
        nutrition_saturated_fat = request.POST.get("nutrition_saturated_fat")
        nutrition_trans_fat = request.POST.get("nutrition_trans_fat")
        nutrition_protein = request.POST.get("nutrition_protein")

        # 알레르기 정보
        allergy_wheat = request.POST.get("allergy_wheat") == "on"
        allergy_milk = request.POST.get("allergy_milk") == "on"
        allergy_egg = request.POST.get("allergy_egg") == "on"
        allergy_soybean = request.POST.get("allergy_soybean") == "on"
        allergy_nuts = request.POST.get("allergy_nuts") == "on"
        allergy_etc = request.POST.get("allergy_etc", "")

        # 이미지 업로드
        item_image = None
        if 'item_image' in request.FILES:
            item_image = request.FILES['item_image']

        # 제품 정보 입력 검수
        if not all([item_name, category, description, cost_price, sale_price, store]):
            return render(request, 'menu/new_menu.html', {
                'error': '기본 정보의 모든 필드를 입력해주세요.'
            })

        try:
            menu = Item(
                best=best,
                new=new,
                show=show,
                item_name=item_name,
                category=category,
                store=store,
                description=description,
                cost_price=cost_price,
                sale_price=sale_price,
                item_image=item_image
            )
            menu.save()

            # 영양 정보
            if all([nutrition_weight, nutrition_calories, nutrition_sodium, nutrition_sugar,
                    nutrition_carbohydrates, nutrition_saturated_fat, nutrition_trans_fat, nutrition_protein]):
                nutrition = NutritionInfo(
                    item_id=menu.item_id,
                    nutrition_weight=nutrition_weight,
                    nutrition_calories=nutrition_calories,
                    nutrition_sodium=nutrition_sodium,
                    nutrition_sugar=nutrition_sugar,
                    nutrition_carbohydrates=nutrition_carbohydrates,
                    nutrition_saturated_fat=nutrition_saturated_fat,
                    nutrition_trans_fat=nutrition_trans_fat,
                    nutrition_protein=nutrition_protein
                )
                nutrition.save()
            else:
                # 영양 정보 입력 검수
                menu.delete()
                return render(request, 'menu/new_menu.html', {
                    'error': '영양 정보의 모든 필드를 입력해주세요.'
                })

            # 영양 정보 등록
            allergy = Allergy(
                item_id=menu.item_id,
                allergy_wheat=allergy_wheat,
                allergy_milk=allergy_milk,
                allergy_egg=allergy_egg,
                allergy_soybean=allergy_soybean,
                allergy_nuts=allergy_nuts,
                allergy_etc=allergy_etc
            )
            allergy.save()

            return redirect('menu_store_menu_info')

        except Exception as e:
            return render(request, 'menu/new_menu.html', {
                'error': f'저장 중 오류가 발생했습니다: {str(e)}'
            })
    else:
        return render(request, 'menu/new_menu.html')