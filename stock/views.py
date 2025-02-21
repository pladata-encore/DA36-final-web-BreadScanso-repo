from django.shortcuts import render
from django.views.decorators.http import require_POST

from menu.models import Item
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from stock.models import Ingredient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def stock_main(request):
    return render(request, 'stock/stock_main.html')  # 메인

def stock_product(request):
    store_filter = request.GET.get('store', '')
    category_filter = request.GET.get('category', '')  # 수정된 부분
    sort_by = request.GET.get('sort', 'item_id')  # 정렬 기준 (기본값: item_id)
    order = request.GET.get('order', 'asc')  # 오름차순/내림차순 (기본값: asc)

    # 필터링
    items = Item.objects.all()
    if store_filter:
        items = items.filter(store=store_filter)
    if category_filter:  # 카테고리 필터링
        items = items.filter(category=category_filter)

    # 정렬 처리
    if order == 'desc':
        sort_by = f"-{sort_by}"
    items = items.order_by(sort_by)

    # 페이지네이션 처리 (10개씩)
    paginator = Paginator(items, 10)
    # 페이지 번호 가져오기, 유효하지 않으면 1 페이지로 설정
    page_number = request.GET.get('page', 1)
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
    return render(request, 'stock/stock_product.html', {'page_obj': page_obj})


@csrf_exempt
def update_stock(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            item_id = data.get('item_id')
            new_stock = int(data.get('new_stock'))

            # 재고 수량 업데이트
            item = Item.objects.get(item_id=item_id)
            item.stock = new_stock
            item.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})



def stock_product_edit(request):
    return render(request, 'stock/stock_product_edit.html')  # 제품 수정

def stock_product_new(request):
    return render(request, 'stock/stock_product_new.html')  # 제품 신규등록

def stock_ingredient(request):
    store_filter = request.GET.get('store', '')
    sort_by = request.GET.get('sort', 'ingredient_id')  # 정렬 기준
    order = request.GET.get('order', 'asc')  # 오름차순/내림차순 (기본값: asc)

    ingredients = Ingredient.objects.all()
    if store_filter:
        ingredients = ingredients.filter(store=store_filter)

    if order == 'desc':
        sort_by = f"-{sort_by}"
    ingredients = ingredients.order_by(sort_by)
    paginator = Paginator(ingredients, 10)
    page_number = request.GET.get('page', 1)
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
    return render(request, 'stock/stock_ingredient.html', {'page_obj': page_obj})

@csrf_exempt
def update_stock_ingredient(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            ingredient_id = data.get('ingredient_id')
            new_stock = int(data.get('new_stock'))

            # 재고 수량 업데이트
            ingredient = Ingredient.objects.get(ingredient_id=ingredient_id)
            ingredient.stock = new_stock
            ingredient.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})




def stock_ingredient_edit(request):
    return render(request, 'stock/stock_ingredient_edit.html')  # 재료 수정

def stock_ingredient_new(request):
    return render(request, 'stock/stock_ingredient_new.html')  # 재료 신규등록
