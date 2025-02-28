import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import Item, NutritionInfo, Allergy
import json
from .utils import upload_product_image_to_s3

# 소비자 화면 메뉴 정보 페이지
def menu_main(request):
    selected_store = request.GET.get('store', '')
    category_filter = request.GET.get('category', '')

    # 기본 쿼리: show=1인 아이템
    items_query = Item.objects.filter(show=1)
    new_items_query = Item.objects.filter(show=1, new=1)

    # 매장이 선택되었다면 필터링
    if selected_store:
        items_query = items_query.filter(store=selected_store).order_by('item_name')
        new_items_query = new_items_query.filter(store=selected_store)

    # 카테고리 필터링 추가
    if category_filter:
        items_query = items_query.filter(category=category_filter)

    # 중복된 item_name 제거 로직 (매장 선택 전용)
    def get_unique_items(query):
        seen_names = set()
        unique_items = []
        for item in query:
            if item.item_name not in seen_names:
                seen_names.add(item.item_name)
                unique_items.append(item)
        return unique_items

    # 매장 선택 여부에 따라 처리
    if not selected_store:
        items = get_unique_items(items_query)
        new_items = get_unique_items(new_items_query)
        best_items = []  # 매장 미선택 시 Best는 표시 안 함
    else:
        items = items_query.distinct()
        new_items = new_items_query.distinct()
        best_items = items_query.filter(best=1).distinct()

    context = {
        'items': items,
        'new_items': new_items,
        'best_items': best_items,
        'selected_store': selected_store,
        'category_filter': category_filter,
    }
    return render(request, 'menu/menu_main.html', context)

# ---------------------------------------------------------------------------- #
# 소비자 화면 제품 상세 페이지
def product_detail(request, item_id):
    item = get_object_or_404(Item, pk=item_id)  # 해당 item_id의 제품을 가져옴
    nutrition_info = NutritionInfo.objects.filter(item_id=item_id).first() # NutritionInfo에서 해당 item_id의 영양 정보 가져오기
    allergy_info = Allergy.objects.filter(item_id=item_id).first() # AllergyInfo에서 해당 item_id의 영양 정보 가져오기
    return render(request, 'menu/product_detail.html', {'item': item, 'nutrition': nutrition_info, 'allergy': allergy_info})


# ---------------------------------------------------------------------------- #
# 점주의 메뉴관리 메인 페이지
def menu_store(request):
    # 현재 로그인한 멤버의 가게 정보 가져오기
    member = request.user.member
    store = member.store

    # 해당 가게의 아이템만 필터링하여 가져오기
    items = Item.objects.filter(store=store).order_by("item_name")

    # 필터링
    category_filter = request.GET.get('category', '')
    show_filter = request.GET.get('show', '')
    best_filter = request.GET.get('best', '')
    new_filter = request.GET.get('new', '')

    if category_filter:
        items = items.filter(category=category_filter)
    if show_filter:
        items = items.filter(show=show_filter == "1")
    if best_filter:
        items = items.filter(best=best_filter == "1")
    if new_filter:
        items = items.filter(new=new_filter == "1")

    # 페이지당 항목 수 (고정)
    items_per_page = 10

    # 페이지네이션 처리
    paginator = Paginator(items, items_per_page)

    # 페이지 번호 가져오기
    page_number = request.GET.get("page", 1)
    try:
        page_number = int(page_number)
        if page_number < 1:
            page_number = 1
    except ValueError:
        page_number = 1

    # 페이지 객체 가져오기
    try:
        page_obj = paginator.page(page_number)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # 페이지 범위 계산
    max_pages = 5
    current_page = page_obj.number
    total_pages = paginator.num_pages

    start_page = max(1, current_page - 2)
    end_page = min(total_pages, start_page + max_pages - 1)

    if end_page - start_page + 1 < max_pages and start_page > 1:
        start_page = max(1, end_page - max_pages + 1)

    page_range = range(start_page, end_page + 1)

    context = {
        'items': page_obj,
        'page_obj': page_obj,
        'page_range': page_range,
        'member': member,
        'category_filter': category_filter,
        'show_filter': show_filter,
        'best_filter': best_filter,
        'new_filter': new_filter,
        'total_items': items.count(),  # 총 아이템 수
    }

    return render(request, 'menu/menu_store.html', context)

# ---------------------------------------------------------------------------- #
# 점주 신규 메뉴 등록 페이지
def menu_add(request):
    member = request.user.member
    return render(request, 'menu/new_menu.html', {'member': member})

# 점주 메뉴 관리 상세 페이지
def menu_store_menu_info(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    nutrition_info = NutritionInfo.objects.filter(item_id=item_id).first()
    allergy_info = Allergy.objects.filter(item_id=item_id).first()

    member = request.user.member

    context = {
        'item': item,
        'nutrition': nutrition_info,
        'allergy': allergy_info,
        'member': member
    }

    return render(request, 'menu/menu_info.html', context)

# 점주 메뉴 관리 수정 페이지
@require_http_methods(["GET", "POST"])
def menu_store_menu_edit(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    if request.method == "POST":
        # 제품 정보 업데이트
        item.item_name = request.POST.get("item_name", item.item_name)
        item.description = request.POST.get("item_info", item.description)
        item.cost_price = request.POST.get("cost", item.cost_price)
        item.sale_price = request.POST.get("price", item.sale_price)
        item.category = request.POST.get("category", item.category)
        item.store = request.POST.get("store", item.store)

        # Best, New, 노출 여부 업데이트
        item.best = request.POST.get("best") == "on"
        item.new = request.POST.get("new") == "on"
        item.show = request.POST.get("show") == "on"

        # **이미지 업로드 로직 추가**
        if 'item_image' in request.FILES:  # 새 이미지 업로드 확인
            try:
                new_image_url = upload_product_image_to_s3(request.FILES['item_image'])
                item.item_image = new_image_url  # S3 URL로 업데이트
            except Exception as e:
                return render(request, "menu/menu_edit.html", {
                    "item": item,
                    "nutrition": NutritionInfo.objects.filter(item=item).first(),
                    "allergy": Allergy.objects.filter(item=item).first(),
                    "error": f"이미지 업로드 중 오류 발생: {str(e)}"
                })

        item.save()  # 제품 정보 저장

        # **영양 정보 업데이트 (있으면 수정, 없으면 추가하지 않음)**
        nutrition_info = NutritionInfo.objects.filter(item=item).first()
        if nutrition_info:
            nutrition_info.nutrition_weight = request.POST.get("nutrition_weight", nutrition_info.nutrition_weight)
            nutrition_info.nutrition_calories = request.POST.get("nutrition_calories", nutrition_info.nutrition_calories)
            nutrition_info.nutrition_sodium = request.POST.get("nutrition_sodium", nutrition_info.nutrition_sodium)
            nutrition_info.nutrition_sugar = request.POST.get("nutrition_sugar", nutrition_info.nutrition_sugar)
            nutrition_info.nutrition_carbohydrates = request.POST.get("nutrition_carbohydrates", nutrition_info.nutrition_carbohydrates)
            nutrition_info.nutrition_saturated_fat = request.POST.get("nutrition_saturated_fat", nutrition_info.nutrition_saturated_fat)
            nutrition_info.nutrition_trans_fat = request.POST.get("nutrition_trans_fat", nutrition_info.nutrition_trans_fat)
            nutrition_info.nutrition_protein = request.POST.get("nutrition_protein", nutrition_info.nutrition_protein)
            nutrition_info.save()

        # **알레르기 정보 업데이트 (있으면 수정, 없으면 추가하지 않음)**
        allergy_info = Allergy.objects.filter(item=item).first()
        if allergy_info:
            allergy_info.allergy_wheat = request.POST.get("allergy_wheat") == "on"
            allergy_info.allergy_milk = request.POST.get("allergy_milk") == "on"
            allergy_info.allergy_egg = request.POST.get("allergy_egg") == "on"
            allergy_info.allergy_soybean = request.POST.get("allergy_soybean") == "on"
            allergy_info.allergy_nuts = request.POST.get("allergy_nuts") == "on"
            allergy_info.allergy_etc = request.POST.get("allergy_etc", allergy_info.allergy_etc)
            allergy_info.save()

        return redirect("menu_store_menu_info", item_id=item.item_id)

    # **기존 데이터 불러오기**
    nutrition_info = NutritionInfo.objects.filter(item=item).first()
    allergy_info = Allergy.objects.filter(item=item).first()
    member = request.user.member

    context = {
        'item': item,
        'nutrition': nutrition_info,
        'allergy': allergy_info,
        'member': member
    }

    return render(request, "menu/menu_edit.html", context)


# 점주 메뉴 관리에서 메뉴 삭제 기능
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


# 신규 제품 등록 기능
# @require_http_methods(["POST"])
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

        # S3
        item_image_url = None
        if 'item_image' in request.FILES:
            try:
                item_image_url = upload_product_image_to_s3(request.FILES['item_image'])
            except Exception as e:
                return render(request, 'menu/new_menu.html', {
                    'error': f'이미지 업로드 중 오류가 발생했습니다: {str(e)}'
                })

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
                item_image=item_image_url
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

            return redirect('menu_store_menu_info', item_id=menu.item_id)

        except Exception as e:
            return render(request, 'menu/new_menu.html', {
                'error': f'저장 중 오류가 발생했습니다: {str(e)}'
            })
    else:
        return render(request, 'menu/new_menu.html')