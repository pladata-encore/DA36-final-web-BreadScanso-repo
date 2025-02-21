from django.urls import path
from . import views  # views.py에서 함수 가져오기

urlpatterns = [
    path('', views.stock_main, name='stock_main'),  # /stock/
    path('product', views.stock_product, name='stock_product'),  # 제품 메인
    path('product/update_stock/', views.update_stock, name='update_stock'),
    path('product/edit', views.stock_product_edit, name='stock_product_edit'),  # 제품 수정
    path('product/new', views.stock_product_new, name='stock_product_new'),  # 제품 신규 등록
    path('ingredient', views.stock_ingredient, name='stock_ingredient'),  # 제품 메인
    path('ingredient/edit', views.stock_ingredient_edit, name='stock_ingredient_edit'),  # 제품 수정
    path('ingredient/new', views.stock_ingredient_new, name='stock_ingredient_new'),  # 제품 신규 등록
]