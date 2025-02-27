from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from menu.models import Item
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from stock.models import Ingredient
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def stock_main(request):
    return render(request, 'stock/stock_main.html')  # 메인


def stock_product(request):
    member = request.user.member
    store = member.store
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    sort_by = request.GET.get('sort', 'item_name')
    order = request.GET.get('order', 'asc')

    # 여기를 수정: 모든 아이템이 아닌 멤버의 스토어에 속한 아이템만 가져오기
    items = Item.objects.filter(store=store)

    # 검색
    if search_query:
        items = items.filter(item_name__icontains=search_query)
    # 필터링
    if category_filter:
        items = items.filter(category=category_filter)
    # 정렬 처리
    if order == 'desc':
        sort_by = f"-{sort_by}"
    items = items.order_by(sort_by)

    # 나머지 코드는 동일
    items_per_page = 10
    paginator = Paginator(items, items_per_page)
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
        page_obj = paginator.get_page(paginator.num_pages)

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
        'search_query': search_query,
        'category_filter': category_filter,  # HTML에서 사용되므로 추가
        'member': member,
        'total_items': items.count(),
    }

    return render(request, 'stock/stock_product.html', context)


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
    search_query = request.GET.get('search', '')
    sort_by = request.GET.get('sort', 'ingredient_name')  # 정렬 기준 (기본값: ingredient_name)
    order = request.GET.get('order', 'asc')  # 오름차순/내림차순 (기본값: asc)

    ingredients = Ingredient.objects.all()

    # 검색
    if search_query:
        ingredients = ingredients.filter(ingredient_name__icontains=search_query)

    # 정렬 처리
    if order == 'desc':
        sort_by = f"-{sort_by}"
    ingredients = ingredients.order_by(sort_by)

    # 페이지네이션
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
    return render(request, 'stock/stock_ingredient.html', {'page_obj': page_obj, 'search_query':search_query})

@csrf_exempt  # CSRF 인증을 비활성화하거나 활성화하는 방식
def update_stock_ingredient(request):
    if request.method == 'POST':
        try:
            # POST로 넘어오는 데이터
            data = json.loads(request.body)
            ingredient_id = data.get('ingredient_id')  # 재료 ID
            new_name = data.get('new_ingredient_name')  # 새로운 제품명
            new_store = data.get('new_store')  # 새로운 매장
            new_stock = int(data.get('new_stock'))  # 새로운 재고 수량

            # 유효성 검사
            if not ingredient_id or not new_name or not new_store or new_stock is None or new_stock < 0:
                return JsonResponse({'success': False, 'error': 'Invalid data provided'})

            # 재료 존재 여부 확인
            try:
                ingredient = Ingredient.objects.get(ingredient_id=ingredient_id)
            except Ingredient.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Ingredient not found'})

            # 재료 정보 업데이트
            ingredient.ingredient_name = new_name
            ingredient.store = new_store
            ingredient.stock = new_stock
            ingredient.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def stock_ingredient_edit(request):
    return render(request, 'stock/stock_ingredient_edit.html')  # 재료 수정

@require_http_methods(["POST"])
def delete_ingredients(request):
    try:
        # 요청 데이터 파싱
        data = json.loads(request.body)
        ingredient_ids = data.get("ingredient_ids", [])

        if not ingredient_ids:
            return JsonResponse({
                "success": False,
                "message": "삭제할 항목이 없습니다."
            })

        # 선택된 재료들 삭제
        deleted_count, _ = Ingredient.objects.filter(ingredient_id__in=ingredient_ids).delete()

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


def stock_ingredient_new(request):
    if request.method == 'POST':
        ingredient_name = request.POST.get('ingredient_name')
        store = request.POST.get('store')
        stock = request.POST.get('stock')

        if ingredient_name and store and stock:
            ingredient = Ingredient(ingredient_name=ingredient_name, store=store, stock=stock)
            ingredient.save()
            return redirect('stock_ingredient')  # 저장 후 재료 페이지로 !

        else:
            # 빈 칸이 있을 경우
            return render(request, 'stock/stock_ingredient_new.html', {
                'error': '모든 필드를 입력해주세요.'
            })
    else:
        member = request.user.member

        return render(request, 'stock/stock_ingredient_new.html', {'member': member})
