from django.shortcuts import render

def stock_main(request):
    return render(request, 'stock/stock_main.html')  # 메인

def stock_product(request):
    return render(request, 'stock/stock_product.html')  # 제품

def stock_product_edit(request):
    return render(request, 'stock/stock_product_edit.html')  # 제품 수정

def stock_product_new(request):
    return render(request, 'stock/stock_product_new.html')  # 제품 신규등록

def stock_ingredient(request):
    return render(request, 'stock/stock_ingredient.html')  # 재료

def stock_ingredient_edit(request):
    return render(request, 'stock/stock_ingredient_edit.html')  # 재료 수정

def stock_ingredient_new(request):
    return render(request, 'stock/stock_ingredient_new.html')  # 재료 신규등록
